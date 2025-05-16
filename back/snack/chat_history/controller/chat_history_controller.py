from django.http import JsonResponse
from rest_framework import viewsets
from account_profile.entity.account_profile import AccountProfile
from chat_history.service.chat_history_service_impl import ChatHistoryServiceImpl

class ChatHistoryController(viewsets.ViewSet):
    __chatHistoryService = ChatHistoryServiceImpl()

    def saveChatHistory(self, request):
        account_id = request.headers.get("Account-ID")
        if not account_id:
            return JsonResponse({"success": False, "error": "Unauthorized"}, status=401)

        author = AccountProfile.objects.get(account__id=account_id)
        user_message = request.data.get("user_message")
        bot_response = request.data.get("bot_response")

        self.__chatHistoryService.saveChatHistory(author, user_message, bot_response)
        return JsonResponse({"success": True, "message": "Chat history saved successfully"}, status=201)

    def getAllChatHistory(self, request):
        account_id = request.headers.get("Account-ID")
        author = AccountProfile.objects.get(account__id=account_id)
        history = self.__chatHistoryService.getAllChatHistory(author)
        return JsonResponse(history, status=200)

    def getRecentChatHistory(self, request):
        account_id = request.headers.get("Account-ID")
        author = AccountProfile.objects.get(account__id=account_id)
        history = self.__chatHistoryService.getRecentChatHistory(author)
        return JsonResponse({"success": True, "history": history}, status=200)
