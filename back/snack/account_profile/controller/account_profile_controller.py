from django.http import JsonResponse
from rest_framework import viewsets, status

from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class AccountProfileController(viewsets.ViewSet):
    __profileService = AccountProfileServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def createProfile(self, request):
        """AccountProfile을 생성하는 엔드포인트"""
        postRequest = request.data
        email = postRequest.get("email")

        # Redis에서 account_id 가져오기
        account_id = self.redisCacheService.getValueByKey(email)

        if not account_id:
            return JsonResponse({"error": "해당 이메일에 대한 계정 정보를 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)

        profile = self.__profileService.createAccountProfile(
            account_id=account_id,
            account_name=postRequest.get("account_name"),
            account_nickname=postRequest.get("account_nickname"),
            phone_num=postRequest.get("phone_num"),
            account_add=postRequest.get("account_add"),
            account_sex=postRequest.get("account_sex"),
            account_birth=postRequest.get("account_birth"),
            account_pay=postRequest.get("account_pay"),
            account_sub=postRequest.get("account_sub")
        )
        return JsonResponse({"success": True, "profile_id": profile.account.id}, status=status.HTTP_201_CREATED)

    def getProfile(self, request):
        account_id = request.headers.get("account-id")
        user_token = request.headers.get("usertoken")

        print(f"account_id: {account_id}")
        print(f"user_token: {user_token}")

        if not user_token or not account_id:
            return JsonResponse({"error": "userToken과 account_id가 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        print(123)

        redis_account_id = self.redisCacheService.getValueByKey(user_token)
        if str(redis_account_id) != str(account_id):
            return JsonResponse({"error": "토큰 인증 실패", "success": False}, status=status.HTTP_403_FORBIDDEN)

        profile = self.__profileService.getProfileByAccountId(account_id)

        if not profile:
            return JsonResponse({"error": "프로필을 찾을 수 없습니다", "success": False}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({
            "account_id": profile["account_id"],
            "account_name": profile["account_name"],
            "account_nickname": profile["account_nickname"],
            "phone_num": profile["phone_num"],
            "account_add": profile["account_add"],
            "account_sex": profile["account_sex"],
            "account_birth": profile["account_birth"],
            "account_pay": profile["account_pay"],
            "account_sub": profile["account_sub"],
            "account_age": profile["account_age"],
            "success": True
        }, status=status.HTTP_200_OK)
    
    def updateProfile(self, request):
        account_id = request.headers.get("account-id")
        user_token = request.headers.get("usertoken")

        if not account_id or not user_token:
            return JsonResponse({"error": "Account-Id와 userToken이 필요합니다.", "success": False}, status=400)

        redis_account_id = self.redisCacheService.getValueByKey(user_token)
        if str(redis_account_id) != str(account_id):
            return JsonResponse({"error": "토큰 인증 실패", "success": False}, status=403)

        post_data = request.data
        updated_profile = self.__profileService.updateProfile(account_id, post_data)

        return JsonResponse({"success": True, "account_id": updated_profile.account.id}, status=200)

