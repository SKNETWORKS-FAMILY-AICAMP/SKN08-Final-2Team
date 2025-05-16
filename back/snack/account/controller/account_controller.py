from django.http import JsonResponse
from rest_framework import viewsets, status
from datetime import datetime, timedelta
from account.service.account_service_impl import AccountServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl
from rest_framework.response import Response

class AccountController(viewsets.ViewSet):
    __accountService = AccountServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def createAccount(self, request):
        """새로운 계정을 생성하는 엔드포인트"""
        postRequest = request.data
        email = postRequest.get("email")
        account_path = postRequest.get("account_path")
        role_type = postRequest.get("role_type", "user")  # 기본값: user

        if not email or not account_path:
            return JsonResponse({"error": "email과 account_path가 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        if self.__accountService.checkEmailDuplication(email):
            return JsonResponse({"error": "이미 존재하는 이메일입니다", "success": False}, status=status.HTTP_409_CONFLICT)

        account = self.__accountService.createAccount(email, account_path, role_type)

        # Redis에 계정 ID 저장 (key: email, value: account_id)
        self.redisCacheService.storeKeyValue(email, account.id)

        return JsonResponse({"success": True, "account_id": account.id}, status=status.HTTP_201_CREATED)

    def getAccount(self, request):
        account_id = request.headers.get("account-id")  
        user_token = request.headers.get("userToken")

        if not user_token or not account_id:
            return JsonResponse({"error": "userToken과 account_id가 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        redis_account_id = self.redisCacheService.getValueByKey(user_token)
        if str(redis_account_id) != str(account_id):
            return JsonResponse({"error": "토큰 인증 실패", "success": False}, status=status.HTTP_403_FORBIDDEN)

        account = self.__accountService.findAccountById(account_id)
        if not account:
            return JsonResponse({"error": "계정을 찾을 수 없습니다", "success": False}, status=status.HTTP_404_NOT_FOUND)

        decrypted_email = self.__decryptEmail(account)

        return JsonResponse({
            "account_id": account.id,
            "email": decrypted_email,
            "role_type": account.role_type.role_type,
            "account_register": account.account_register.strftime('%Y-%m-%d %H:%M:%S'),
            "account_used_date": account.account_used_date.strftime('%Y-%m-%d %H:%M:%S'),
            "account_path": account.account_path,
            "account_status": account.account_status,
            "success": True
        }, status=status.HTTP_200_OK)

    def updateLastUsed(self, request, email):
        """이메일 기반으로 Redis에서 account_id를 가져와 마지막 로그인 날짜 업데이트"""
        account_id = self.redisCacheService.getValueByKey(email)

        if not account_id:
            return JsonResponse({"error": "해당 이메일에 대한 계정 정보를 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)

        updated_account = self.__accountService.updateLastUsed(account_id)

        if not updated_account:
            return JsonResponse({"error": "계정을 찾을 수 없습니다", "success": False}, status=status.HTTP_404_NOT_FOUND)

        self.redisCacheService.storeKeyValue(email, account_id)
        
        return JsonResponse({
            "message": "최근 사용 날짜가 업데이트되었습니다.",
            "last_used_date": updated_account.account_used_date.strftime('%Y-%m-%d %H:%M:%S'),
            "success": True
        }, status=status.HTTP_200_OK)

    # 이메일 복호화
    def __decryptEmail(self, account):
        try:
            decrypted_email = account.get_decrypted_email()
            print(f"복호화된 이메일: {decrypted_email}")
            return decrypted_email
        except Exception as e:
            print(f"[ERROR] 이메일 복호화 실패: {str(e)}")
            return account.email  # fallback: 암호화 된 그대로 반환

    # 관리자 로그인, 권한 확인
    def __checkAdminPermission(self, user_token):
        # 유저 토큰 확인
        if not user_token:
            return None, JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        # 관리자 계정 로그인 확인
        admin_account_id = self.redisCacheService.getValueByKey(user_token)
        if not admin_account_id:
            return None, JsonResponse({"error": "로그인이 필요합니다.", "success": False}, status=status.HTTP_401_UNAUTHORIZED)

        # 관리자 권한 확인
        admin_account = self.__accountService.findAccountById(admin_account_id)
        if not admin_account or admin_account.role_type.role_type != 'ADMIN':
            return None, JsonResponse({"error": "관리자 권한이 필요합니다.", "success": False}, status=status.HTTP_403_FORBIDDEN)

        return admin_account, None

    #  관리자 -사용자 계정 정지 요청(SUSPEND)
    def suspendAccount(self, request):
        user_token = request.headers.get("userToken")
        target_account_id = request.data.get("target_account_id")
        reason = request.data.get("reason", "정지 사유")
        duration = request.data.get("duration")  # 정지 기간 일수 (정수)

        admin_account, error_response = self.__checkAdminPermission(user_token)
        if error_response:
            return error_response  # 관리자 로그인, 권한 확인

        # 대상 사용자 확인
        target_account = self.__accountService.findAccountById(target_account_id)
        if not target_account:
            return Response({"error": "대상 사용자를 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)

        # 영구 탈퇴 여부 확인
        if target_account.account_status == 4:
            return JsonResponse({"error": "대상 사용자는 영구 탈퇴 상태 입니다.", "success": False},
                                status=status.HTTP_400_BAD_REQUEST)

        # 대상 사용자 정지 상태 확인 (이미 정지된 사용자 확인)
        is_suspended, message = self.__accountService.isSuspended(target_account_id)
        if is_suspended:
            return Response({"error": message, "success": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            suspended_account = self.__accountService.suspendAccountById(
                target_account_id=target_account_id,
                reason=reason,
                duration=int(duration) if duration else None
            )
            decrypted_email = self.__decryptEmail(suspended_account)

            return Response({
                "success": True,
                "message": f"사용자 {decrypted_email} (ID: {suspended_account.id})이 정지되었습니다.",
                "reason": suspended_account.suspension_reason,
                "suspended_until": suspended_account.suspended_until.strftime(
                    '%Y-%m-%d %H:%M:%S') if suspended_account.suspended_until else "무기한 정지"
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e), "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 관리자 -정지된 사용자 계정을 해제
    def unsuspendAccount(self, request, account_id):
        user_token = request.headers.get("userToken")
        target_account = self.__accountService.findAccountById(account_id)  # URL에서 받아온 account_id 사용

        if not target_account:
            return JsonResponse({"error": "대상 사용자를 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)

        admin_account, error_response = self.__checkAdminPermission(user_token)
        if error_response:
            return error_response

        # 정지 여부 확인
        if target_account.account_status != 1:
            return JsonResponse({"error": "대상 사용자가 계정 정지 된 상태가 아닙니다.", "success": False},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            self.__accountService.unsuspendAccountById(account_id)
            return Response({"success": True, "message": "사용자 계정의 정지가 해제되었습니다."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


      # 관리자 -정지된 사용자 목록 조회
    def getSuspendedAccounts(self, request):
        user_token = request.headers.get("userToken")

        admin_account, error_response = self.__checkAdminPermission(user_token)
        if error_response:
            return error_response

        try:
            suspended_accounts = self.__accountService.getSuspendedAccounts()
            result = []

            for account in suspended_accounts:
                try:
                    decrypted_email = self.__decryptEmail(account)
                except Exception as e:
                    print(f"[ERROR] 이메일 복호화 실패: {str(e)}")
                    decrypted_email = account.email  # 복호화 실패 시 원래 이메일 유지

                result.append({
                    "id": account.id,
                    "email": decrypted_email,
                    "reason": account.suspension_reason,
                    "suspended_until": account.suspended_until.strftime(
                        '%Y-%m-%d %H:%M:%S') if account.suspended_until else "무기한 정지"
                })
            return Response({"success": True, "suspended_accounts": result}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e), "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 관리자 -사용자 계정 차단 (BAN, 영구 탈퇴)
    def banAccount(self, request):
        user_token = request.headers.get("userToken")
        target_account_id = request.data.get("target_account_id")
        reason = request.data.get("reason", "차단 사유")

        admin_account, error_response = self.__checkAdminPermission(user_token)
        if error_response:
            return error_response

        if not target_account_id:
            return JsonResponse({"error": "target_account_id가 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        # 대상 사용자 계정 확인
        target_account = self.__accountService.findAccountById(target_account_id)
        if not target_account:
            return JsonResponse({"error": "대상 사용자를 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)

        # 영구탈퇴 여부 확인
        if target_account.account_status == 4:
            return JsonResponse({"error": "이미 영구탈퇴 된 사용자 입니다.", "success": False},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            banned_account = self.__accountService.banAccountById(target_account_id, reason)
            decrypted_email = self.__decryptEmail(banned_account)
            return Response({
                "success": True,
                "message": f"사용자 {decrypted_email} (ID: {banned_account.id})이 차단되었습니다.",
                "reason": banned_account.suspension_reason
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e), "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 관리자 -차단 사용자 차단 해제
    def unbanAccount(self, request, account_id):  # URL에서 account_id 직접 받기
        user_token = request.headers.get("userToken")

        admin_account, error_response = self.__checkAdminPermission(user_token)
        if error_response:
            return error_response

        # 대상 사용자 확인
        target_account = self.__accountService.findAccountById(account_id)  # URL에서 받아온 account_id 사용
        if not target_account:
            return JsonResponse({"error": "대상 사용자를 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)

        # 영구 탈퇴 여부 확인
        if target_account.account_status != 4:
            return JsonResponse({"error": "대상 사용자가 영구탈퇴 된 상태가 아닙니다.", "success": False},
                                status=status.HTTP_400_BAD_REQUEST)
        try:
            self.__accountService.unbanAccountById(account_id)
            return Response({"success": True, "message": "사용자 계정의 영구 탈퇴가 해제되었습니다."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    # 관리자 -차단 사용자 목록 요청
    def getBannedAccounts(self, request):
        user_token = request.headers.get("userToken")

        admin_account, error_response = self.__checkAdminPermission(user_token)
        if error_response:
            return error_response

        try:
            banned_accounts = self.__accountService.getBannedAccounts()
            banned_list = []

            for account in banned_accounts:
                try:
                    decrypted_email = self.__decryptEmail(account)
                except Exception as e:
                    print(f"[ERROR] 이메일 복호화 실패: {str(e)}")
                    decrypted_email = account.email  # 복호화 실패 시 원래 이메일 유지

                banned_list.append({
                    "id": account.id,
                    "email": decrypted_email,
                    "banned_reason": account.banned_reason
                })
            return Response({"success": True, "banned_accounts": banned_list}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e), "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)