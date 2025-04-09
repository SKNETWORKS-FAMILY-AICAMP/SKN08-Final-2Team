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
    def deactivate_account(self, account_id: int) -> bool:
        pass

    @abstractmethod
    def deleteAccountById(self, account_id: int) -> bool:
        pass