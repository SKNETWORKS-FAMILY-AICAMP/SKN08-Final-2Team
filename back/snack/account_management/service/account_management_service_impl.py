# account_management/service/account_management_service_impl.py
from account.models import Account
from django.utils import timezone
from datetime import timedelta
from account_management.service.account_management_service import AccountManagementService

class AccountManagementServiceImpl:
    def releaseSuspendedAccounts(self):
        now = timezone.now()
        suspended_accounts = Account.objects.filter(
            account_status=1,  # 사용 정지 상태
            suspended_until__lte=now  # 정지 기간이 지난 사용자
        )

        for account in suspended_accounts:
            account.account_status = 0  # 정지 해제
            account.suspended_until = None
            account.suspension_reason = None
            account.save()

    # def deleteExpiredAccounts(self):
    #     threshold_date = timezone.now() - timedelta(days=3 * 365)
    #     expired_accounts = Account.objects.filter(
    #         account_status=0,  # 활성화 상태
    #         account_used_date__lte=threshold_date
    #     )
    #
    #     for account in expired_accounts:
    #         account.delete()