from abc import ABC, abstractmethod
from account.entity.account import Account

class AccountRepository(ABC):

    @abstractmethod
    def save(self, account: Account):
        """새로운 계정을 저장한다."""
        pass

    @abstractmethod
    def findById(self, account_id: int):
        """ID로 계정을 찾는다."""
        pass

    @abstractmethod
    def findByEmail(self, email: str):
        """이메일로 계정을 찾는다."""
        pass

    @abstractmethod
    def updateLastUsed(self, account_id: int):
        """로그인 시 마지막 접속 날짜를 업데이트한다."""
        pass

    @abstractmethod
    def findAccountPath(self, email: str):
        pass

    @abstractmethod
    def updateSuspendedAccountStatus(self, account: Account) -> None:
        pass

    @abstractmethod
    def updateBannedAccountStatus(self, account: Account) -> None:
        pass

    @abstractmethod
    def findSuspendedAccounts(self):
        pass

    @abstractmethod
    def findBannedAccounts(self):
        pass