from datetime import datetime
from typing import List, Optional
from delete_account.entity.delete_account import DeletedAccount
from delete_account.repository.delete_account_repository import DeleteAccountRepository
from account.entity.account import Account, AccountStatus


class DeleteAccountRepositoryImpl(DeleteAccountRepository):
    # # account_status만 변경
    # def deactivateAccount(self, account_id: int) -> bool:
    #     try:
    #         account = Account.objects.get(id=account_id)
    #         account.account_status = AccountStatus.DELETED.value
    #         account.save(update_fields=['account_status'])
    #         return True
    #     except Account.DoesNotExist:
    #         return False
    #
    # # 데이터 베이스에서 삭제
    # def deleteAccountById(self, account_id: int) -> bool:
    #     try:
    #         account = Account.objects.get(id=account_id)
    #         account.delete()
    #         return True
    #     except Account.DoesNotExist:
    #         return False

    def save(self, account_id: int) -> DeletedAccount:
        deleted_account = DeletedAccount(account_id=account_id)
        deleted_account.save()
        return deleted_account

    def findByAccountId(self, account_id: int) -> Optional[DeletedAccount]:
        return DeletedAccount.objects.filter(account_id=account_id).first()

    def findAllBeforeThreshold(self, threshold_date: datetime) -> List[DeletedAccount]:
        return DeletedAccount.objects.filter(deleted_at__lt=threshold_date)

    def delete(self, deleted_account: DeletedAccount) -> None:
        deleted_account.delete()