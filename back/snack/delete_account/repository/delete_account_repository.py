from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from delete_account.entity.delete_account import DeletedAccount

class DeleteAccountRepository(ABC):

    @abstractmethod
    def save(self, account_id: int) -> DeletedAccount:
        pass

    @abstractmethod
    def find_by_account_id(self, account_id: int) -> Optional[DeletedAccount]:
        pass

    @abstractmethod
    def find_all_before_threshold(self, threshold_date: datetime) -> List[DeletedAccount]:
        pass

    @abstractmethod
    def delete(self, deleted_account: DeletedAccount) -> None:
        pass