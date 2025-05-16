from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets, status
from account.service.account_service_impl import AccountServiceImpl
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from account_alarm.service.account_alarm_service_impl import AccountAlarmServiceImpl
from comment.service.comment_service_impl import CommentServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl

class AccountAlarmController(viewsets.ViewSet):
    __accountService = AccountServiceImpl.getInstance()
    # __commentService = CommentServiceImpl.getInstance()
    __accountAlarmService = AccountAlarmServiceImpl.getInstance()
    # __accountProfileService = AccountProfileServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()





    def getUserAlarms(self, request):
        user_token = request.headers.get("userToken")
        if not user_token:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=400)

        account_id = self.redisCacheService.getValueByKey(user_token)
        if not account_id:
            return JsonResponse({"error": "로그인이 필요합니다.", "success": False}, status=401)

        alarms = self.__accountAlarmService.getUserAlarmList(account_id)
        return JsonResponse({"success": True, "data": {"alarms": alarms}}, status=200)


    def readUserAlarm(self, request):
        user_token = request.headers.get("userToken")
        alarm_id = request.data.get("alarm_id")
        # alarm_id = request.headers.get("alarm_id")
        if not user_token:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=400)

        account_id = self.redisCacheService.getValueByKey(user_token)
        if not account_id:
            return JsonResponse({"error": "로그인이 필요합니다.", "success": False}, status=401)

        if not alarm_id:
            return JsonResponse({"error": "alarm_id가 필요합니다.", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.__accountAlarmService.readAlarm(alarm_id)
            return JsonResponse({"success": True, "message": "알림이 읽음 처리되었습니다."}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "알림을 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)





    # account_alarm_status 권한상태 체크 board_title : nickname -> service

    # def __checkUserAccount(self, request):
    #     user_token = request.headers.get("userToken")
    #     if not user_token:
    #         return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=400)
    #
    #     account_id = self.redisCacheService.getValueByKey(user_token)
    #     if not account_id:
    #         return JsonResponse({"error": "로그인이 필요합니다.", "success": False}, status=401)
    #
    #     account = self.__accountService.findAccountById(accout_id)
    #
    #     return user_token, account
    #
    #
    # def markAlarmAsRead(self, request):
    #     user_token = request.headers.get("userToken")
    #     if not user_token:
    #         return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=400)
    #
    #     account_id = self.redisCacheService.getValueByKey(user_token)
    #     if not account_id:
    #         return JsonResponse({"error": "로그인이 필요합니다.", "success": False}, status=401)
    #
    #     alarm_id = request.data.get("alarm_id")
    #     if not alarm_id:
    #         return JsonResponse({"error": "alarm_id가 필요합니다.", "success": False}, status=400)
    #
    #     self.alarm_service.markAlarmAsRead(account_id, alarm_id)
    #     return JsonResponse({"success": True, "message": "알림이 읽음 처리되었습니다."}, status=200)
    #


    # def __checkAlarmStatus(self, account_id):
    #     profile = self.__accountProfileService.getAccountProfile(account_id)
    #     # if not profile:
    #     #     return 0, 0  # 기본값 활성화
    #
    #     # 게시글 댓글과 대댓글 알림 상태 확인
    #     alam_board_status = profile.alam_comment_status if profile.alam_board_status is not None else 0
    #     alam_comment_status = profile.alam_board_status if profile.alam_comment_status is not None else 0
    #     return alam_comment_status, alam_recomment_status