from datetime import datetime
from typing import List, Optional
from delete_account.entity.delete_account import DeletedAccount
from delete_account.repository.delete_account_repository import DeleteAccountRepository

class DeleteAccountRepositoryImpl(DeleteAccountRepository):

    def save(self, account_id: int) -> DeletedAccount:
        deleted_account = DeletedAccount(account_id=account_id)
        deleted_account.save()
        return deleted_account

    def find_by_account_id(self, account_id: int) -> Optional[DeletedAccount]:
        return DeletedAccount.objects.filter(account_id=account_id).first()

    def find_all_before_threshold(self, threshold_date: datetime) -> List[DeletedAccount]:
        return DeletedAccount.objects.filter(deleted_at__lt=threshold_date)

    def delete(self, deleted_account: DeletedAccount) -> None:
        deleted_account.delete()