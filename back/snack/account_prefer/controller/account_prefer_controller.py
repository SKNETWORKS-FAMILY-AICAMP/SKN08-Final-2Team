from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account_prefer.entity.account_prefer import AccountPrefer
from account.entity.account import Account

class SaveAccountPreference(APIView):
    def post(self, request):
        data = request.data
        account_id = data.get("account_id")
        answers = data.get("answers")  # 리스트형

        if not account_id or answers is None:
            return Response({"error": "Missing data"}, status=400)

        try:
            account = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=404)

        prefer, _ = AccountPrefer.objects.get_or_create(account=account)

        for i in range(1, 20):  # Q_1 ~ Q_19
            answer = answers[i - 1] if i - 1 < len(answers) else None
            if isinstance(answer, list):
                setattr(prefer, f"Q_{i}", ', '.join(answer))
            else:
                setattr(prefer, f"Q_{i}", answer)

        prefer.save()
        return Response({"success": True}, status=200)
