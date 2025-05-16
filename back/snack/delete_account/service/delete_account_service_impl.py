from datetime import datetime, timedelta
from delete_account.repository.delete_account_repository_impl import DeleteAccountRepositoryImpl
from account.service.account_service_impl import AccountServiceImpl
from delete_account.service.delete_account_service import DeleteAccountService

class DeleteAccountServiceImpl(DeleteAccountService):
    def __init__(self):
        self.deletedAccountRepository = DeleteAccountRepositoryImpl()
        self.accountService = AccountServiceImpl.getInstance()

    def deactivateAccount(self, account_id: int) -> bool:
        success = self.accountService.deactivateAccount(account_id)
        if success:
            self.deletedAccountRepository.save(account_id)
        return success

    def deleteExpiredAccounts(self) -> None:
        threshold_date = datetime.now() - timedelta(days=365 * 3)
        expired_accounts = self.deletedAccountRepository.findAllBeforeThreshold(threshold_date)

        for deleted_account in expired_accounts:
            self.accountService.deleteAccountById(deleted_account.account_id)
            self.deletedAccountRepository.delete(deleted_account)