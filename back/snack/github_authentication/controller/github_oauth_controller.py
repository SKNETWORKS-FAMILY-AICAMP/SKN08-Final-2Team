import uuid
import random
import os

from django.db import transaction
from django.http import JsonResponse
from rest_framework import viewsets, status

from github_authentication.service.github_oauth_service_impl import GithubOauthServiceImpl
from account.service.account_service_impl import AccountServiceImpl
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl
from account.entity.role_type import RoleType


class GithubOauthController(viewsets.ViewSet):
    githubOauthService = GithubOauthServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()
    accountProfileService = AccountProfileServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def requestGithubOauthLink(self, request):
        url = self.githubOauthService.requestGithubOauthLink()
        return JsonResponse({"url": url}, status=status.HTTP_200_OK)

    def requestAccessToken(self, request):
        code = request.data.get('code')
        if not code:
            return JsonResponse({'error': 'Authorization code is required'}, status=400)

        try:
            tokenResponse = self.githubOauthService.requestAccessToken(code)
            print("🔁 GitHub tokenResponse:", tokenResponse)

            accessToken = tokenResponse.get('access_token')
            if not accessToken:
                return JsonResponse({
                    'error': "'access_token'이 응답에 없습니다.",
                    'token_response': tokenResponse  # 원본 GitHub 응답 함께 반환
                }, status=500)

            with transaction.atomic():
                userInfo = self.githubOauthService.requestUserInfo(accessToken)
                print("✅ userInfo:", userInfo)

                if not userInfo:
                    return JsonResponse({'error': 'GitHub 사용자 정보를 받아오지 못했습니다.'}, status=500)

                email = userInfo.get('email', '')
                if not email:
                    print("❌ GitHub 이메일 없음, fallback 진행 중")
                github_login_name = userInfo.get('login', '')
                print(f"✅ github login name: {github_login_name}")

                account_path = "github"
                role_type = RoleType.USER  # 기본은 일반 사용자

                print("✅ userInfo:", userInfo)

                email = userInfo.get('email', '')
                print(f"✅ email: {email}")

                github_login_name = userInfo.get('login', '')
                print(f"✅ github login: {github_login_name}")

                account = self.accountService.checkEmailDuplication(email)
                if account:
                    conflict_message = self.accountService.checkAccountPath(email, account_path)
                    if conflict_message:
                        return JsonResponse({'success': False, 'error_message': conflict_message}, status=409)
                is_new_account = False

                if account is None:
                    is_new_account = True
                    account = self.accountService.createAccount(email, account_path, role_type)
                    nickname = self.__generateUniqueNickname()
                    self.accountProfileService.createAccountProfile(
                        account.id, github_login_name, nickname, "", "", "", None, "", False
                    )


                # 안전하게 Redis 저장
                email = getattr(account, 'email', None)
                acc_id = getattr(account, 'id', None)

                if not email or not acc_id:
                    return JsonResponse({'error': 'Redis에 저장할 계정 정보가 없습니다.'}, status=500)

                try:
                    self.redisCacheService.storeKeyValue(email, acc_id)
                except Exception as e:
                    print("Redis 저장 오류:", e)
                    return JsonResponse({'error': str(e)}, status=500)

                userToken = f"github-{uuid.uuid4()}"
                self.redisCacheService.storeKeyValue(userToken, account.id)

                self.accountService.updateLastUsed(account.id)
                self.redisCacheService.storeKeyValue(account.email, account.id)
                print(userToken)
                print(account.id)

                response = JsonResponse({'message': 'login_status_ok'}, status=status.HTTP_201_CREATED if is_new_account else status.HTTP_200_OK)
                response['usertoken'] = userToken
                response['account-id'] = account.id
                response["Access-Control-Expose-Headers"] = "usertoken,account-id"
                return response

        except Exception as e:
            import traceback
            print("🚨 예외 발생:")
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    def validateAdminCode(self, request):
        """GitHub 로그인 후 관리자 권한 요청"""
        admin_code = request.data.get("admin_code")
        user_token = request.headers.get("usertoken")
        account_id = request.headers.get("account-id")

        print(f"🔍 admin_code: {admin_code}, user_token: {user_token}, account_id: {account_id}")

        if not admin_code or not user_token or not account_id:
            return JsonResponse({"error": "Missing required headers or admin code"}, status=400)

        email = self.redisCacheService.getValueByKey(user_token)
        if not email:
            return JsonResponse({"error": "유효하지 않은 토큰입니다."}, status=401)

        # .env에서 admin code 불러오기
        expected_admin_code = os.getenv("GITHUB_ADMIN_CODE")
        if admin_code != expected_admin_code:
            return JsonResponse({"success": False, "message": "잘못된 관리자 코드입니다."}, status=403)

        try:
            updated = self.accountService.updateRoleToAdmin(account_id)
            if updated:
                new_nickname = self.__generateAdminNickname()
                self.accountProfileService.updateNicknameByAccountId(account_id, new_nickname)
            return JsonResponse({"success": True, "message": "관리자 권한이 부여되었습니다."}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def __generateUniqueNickname(self):
        base = "헝글"
        for _ in range(10):
            candidate = base + str(random.randint(1000, 9999))
            from account_profile.entity.account_profile import AccountProfile
            if not AccountProfile.objects.filter(account_nickname=candidate).exists():
                return candidate
        return base + str(uuid.uuid4())[:4]

    def __generateAdminNickname(self):
        base = "헝글 관리자"
        from account_profile.entity.account_profile import AccountProfile
        if not AccountProfile.objects.filter(account_nickname=base).exists():
            return base
        suffix = 1
        while True:
            candidate = f"{base} {suffix}"
            if not AccountProfile.objects.filter(account_nickname=candidate).exists():
                return candidate
            suffix += 1
