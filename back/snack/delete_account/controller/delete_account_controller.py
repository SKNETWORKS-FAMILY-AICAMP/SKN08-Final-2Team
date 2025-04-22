from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from delete_account.service.delete_account_service_impl import DeleteAccountServiceImpl

class DeleteAccountController(viewsets.ViewSet):
    __deleteAccountService = DeleteAccountServiceImpl()

    @action(detail=False, methods=["post"])
    def deactivateAccount(self, request):
        account_id = request.data.get("account-id")
        if not account_id:
            return Response({"error": "account_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        success = self.__deleteAccountService.deactivate_account(account_id)
        if success:
            return Response({"message": "계정이 성공적으로 비활성화되었습니다.", "success": True}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "계정 비활성화 실패", "success": False}, status=status.HTTP_404_NOT_FOUND)