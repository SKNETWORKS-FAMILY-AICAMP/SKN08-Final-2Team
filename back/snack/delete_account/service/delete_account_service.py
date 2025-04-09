from abc import ABC, abstractmethod

class DeleteAccountService(ABC):

    @abstractmethod
    def deactivate_account(self, account_id: int) -> bool:
        pass

    @abstractmethod
    def delete_expired_accounts(self) -> None:
        pass