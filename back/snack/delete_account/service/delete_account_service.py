from abc import ABC, abstractmethod

class DeleteAccountService(ABC):

    @abstractmethod
    def deactivateAccount(self, account_id: int) -> bool:
        pass

    @abstractmethod
    def deleteExpiredAccounts(self) -> None:
        pass