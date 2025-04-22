import uuid
import random
from datetime import datetime

from django.db import transaction
from django.http import JsonResponse
from rest_framework import viewsets, status

from meta_authentication.service.meta_oauth_service_impl import MetaOauthServiceImpl
from account.service.account_service_impl import AccountServiceImpl
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl
from account.entity.role_type import RoleType

class MetaOauthController(viewsets.ViewSet):
    metaOauthService = MetaOauthServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()
    accountProfileService = AccountProfileServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def requestMetaOauthLink(self, request):
        url = self.metaOauthService.requestMetaOauthLink()
        return JsonResponse({"url": url}, status=status.HTTP_200_OK)

    def requestAccessToken(self, request):
        code = request.data.get('code')
        if not code:
            return JsonResponse({'error': 'Authorization code is required'}, status=400)

        try:
            tokenResponse = self.metaOauthService.requestAccessToken(code)
            accessToken = tokenResponse['access_token']

            with transaction.atomic():
                userInfo = self.metaOauthService.requestUserInfo(accessToken)
                email = userInfo.get('email', '')
                name = userInfo.get('name', '')
                account_path = "Meta"
                role_type = RoleType.USER
                phone_num = ""
                address = ""
                gender = ""
                birth = None
                payment = ""
                subscribed = False

                userToken = f"meta-{uuid.uuid4()}"
                self.redisCacheService.storeKeyValue(userToken, email)
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
                        account.id, name, nickname, phone_num, address, gender, birth, payment, subscribed
                    )

                self.accountService.updateLastUsed(account.id)
                self.redisCacheService.storeKeyValue(account.email, account.id)

                response = JsonResponse({'message': 'login_status_ok'}, status=status.HTTP_201_CREATED if is_new_account else status.HTTP_200_OK)
                response['usertoken'] = userToken
                response['account_id'] = account.id
                response["Access-Control-Expose-Headers"] = "usertoken,account_id"
                return response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def requestUserToken(self, request):
        access_token = request.data.get('access_token')
        email = request.data.get('email')
        account_path = "Meta"
        role_type = RoleType.USER
        phone_num = request.data.get('phone_num', "")
        address = request.data.get('address', "")
        gender = request.data.get('gender', "")
        birthyear = request.data.get('birthyear', "")
        birthday = request.data.get('birthday', "")
        payment = request.data.get('payment', "")
        subscribed = request.data.get('subscribed', False)

        birth = None
        if birthday and birthyear:
            try:
                birth = datetime.strptime(f"{birthyear}-{birthday}", "%Y-%m-%d").date()
            except ValueError:
                birth = None

        if not access_token or not email:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            with transaction.atomic():
                name = request.data.get('name') or request.data.get('nickname', '')

                account = self.accountService.checkEmailDuplication(email)
                userToken = f"meta-{uuid.uuid4()}"
                self.redisCacheService.storeKeyValue(userToken, email)

                if account:
                    conflict_message = self.accountService.checkAccountPath(email, account_path)
                    if conflict_message:
                        return JsonResponse({'success': False, 'error_message': conflict_message}, status=601)

                is_new_account = False
                if account is None:
                    is_new_account = True
                    account = self.accountService.createAccount(email, account_path, role_type)
                    nickname = self.__generateUniqueNickname()
                    self.accountProfileService.createAccountProfile(
                        account.id, name, nickname, phone_num, address, gender, birth, payment, subscribed
                    )

                self.accountService.updateLastUsed(account.id)
                self.redisCacheService.storeKeyValue(account.email, account.id)

                response = JsonResponse({'message': 'login_status_ok'}, status=status.HTTP_201_CREATED if is_new_account else status.HTTP_200_OK)
                response['userToken'] = userToken
                response['account_id'] = account.id
                return response

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

    def __createUserTokenWithAccessToken(self, account, accessToken):
        try:
            userToken = f"meta-{uuid.uuid4()}"
            self.redisCacheService.storeKeyValue(account.getId(), accessToken)
            self.redisCacheService.storeKeyValue(userToken, account.getId())
            return userToken
        except Exception as e:
            print('Redis에 토큰 저장 중 에러:', e)
            raise RuntimeError('Redis에 토큰 저장 중 에러')
