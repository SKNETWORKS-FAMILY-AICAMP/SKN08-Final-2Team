from abc import ABC, abstractmethod
from account.entity.account import Account

class AccountService(ABC):
    @abstractmethod
    def createAccount(self, email: str, account_path: str, role_type: str) -> Account:
        """새로운 계정을 생성한다."""
        pass

    @abstractmethod
    def checkEmailDuplication(self, email: str) -> bool:
        """이메일 중복 확인"""
        pass

    @abstractmethod
    def findAccountById(self, account_id: int) -> Account:
        """Account ID로 계정을 찾는다."""
        pass

    @abstractmethod
    def updateLastUsed(self, account_id: int):
        """로그인 시 마지막 접속 날짜를 업데이트한다."""
        pass

    @abstractmethod
    def deactivateAccount(self, account_id: int) -> bool:
        pass

    @abstractmethod
    def deleteAccountById(self, account_id: int) -> bool:
        pass

    @abstractmethod
    def checkAccountPath(self, email: str, login_path: str):
        pass

    @abstractmethod
    def updateRoleToAdmin(self, account_id):
        pass

    @abstractmethod
    def suspendAccountById(self, account_id: int, reason: str, duration: int = None):
        pass

    @abstractmethod
    def isSuspended(self, account_id: int):
        pass

    @abstractmethod
    def unsuspendAccountById(self, account_id: int):
        pass

    @abstractmethod
    def getSuspendedAccounts(self):
        pass

    @abstractmethod
    def banAccountById(self, target_account_id: int, reason: str):
        pass

    @abstractmethod
    def getBannedAccounts(self):
        pass

    @abstractmethod
    def unbanAccountById(self, target_account_id: int):
        pass