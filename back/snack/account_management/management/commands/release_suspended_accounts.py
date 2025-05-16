from django.core.management.base import BaseCommand
from account_management.service.account_management_service_impl import AccountManagementServiceImpl

class Command(BaseCommand):
    help = "정지된 사용자의 정지 기간이 지나면 자동으로 정지를 해제합니다."

    def handle(self, *args, **kwargs):
        service = AccountManagementServiceImpl()
        service.releaseSuspendedAccounts()
        self.stdout.write(self.style.SUCCESS("✅ Suspended accounts released successfully."))
