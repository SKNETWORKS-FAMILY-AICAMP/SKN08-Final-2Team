from django.core.management.base import BaseCommand
from delete_account.service.delete_account_service_impl import DeleteAccountServiceImpl

class Command(BaseCommand):
    help = "Delete accounts that were deactivated more than 3 years ago."

    def handle(self, *args, **kwargs):
        service = DeleteAccountServiceImpl()
        service.deleteExpiredAccounts()
        self.stdout.write(self.style.SUCCESS("✅ Expired accounts deleted successfully."))