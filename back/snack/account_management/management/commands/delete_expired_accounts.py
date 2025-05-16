# from django.core.management.base import BaseCommand
# from account_management.service.account_management_service_impl import AccountManagementServiceImpl
#
# class Command(BaseCommand):
#     help = "Delete accounts that were deactivated more than 3 years ago."
#
#     def handle(self, *args, **kwargs):
#         service = AccountManagementServiceImpl()
#         service.deleteExpiredAccounts()
#         self.stdout.write(self.style.SUCCESS("✅ Expired accounts deleted successfully."))
