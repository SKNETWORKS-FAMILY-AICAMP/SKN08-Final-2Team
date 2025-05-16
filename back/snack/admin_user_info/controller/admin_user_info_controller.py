from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from account.entity.account import Account
from admin_user_info.service.admin_user_info_service_impl import AdminUserInfoServiceImpl
from account.service.account_service_impl import AccountServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class AdminUserInfoController(viewsets.ViewSet):
    __accountService = AccountServiceImpl.getInstance()
    __adminUserInfoService = AdminUserInfoServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()


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


    # 관리자가 사용자의 모든 정보를 요청
    def getUserInfo(self, request, account_id):
        user_token = request.headers.get("userToken")
        admin_account, error_response = self.__checkAdminPermission(user_token)
        if error_response:
            return error_response

        user_id = account_id
        target_account = self.__accountService.findAccountById(user_id)
        if not target_account:
            return JsonResponse({"error": "대상 사용자를 찾을 수 없습니다.", "success": False}, status=404)

        user_info = self.__adminUserInfoService.getUserInfo(user_id)
        if not user_info:
            return JsonResponse({"error": "사용자를 찾을 수 없습니다.", "success": False}, status=404)

        return JsonResponse({"success": True, "user_info": user_info}, status=200)


    # 관리자가 모든 사용자들의 정보를 요청
    def getUserInfoList(self, request):
        user_token = request.headers.get("userToken")
        admin_account, error_response = self.__checkAdminPermission(user_token)
        if error_response:
            return error_response

        user_list = self.__adminUserInfoService.getUserInfoList()
        return JsonResponse({"success": True, "user_list": user_list}, status=200)