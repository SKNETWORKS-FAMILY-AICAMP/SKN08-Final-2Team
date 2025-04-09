from django.core.exceptions import ObjectDoesNotExist
from account.entity.account import Account
from account.entity.account_role_type import AccountRoleType
from account.entity.role_type import RoleType
from account.repository.account_repository import AccountRepository
from django.utils.timezone import now
from utility.encryption import AESCipher
aes = AESCipher()

class AccountRepositoryImpl(AccountRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save(self, account: Account):
        """새로운 계정을 저장한다."""
        account.save()
        return account

    def findById(self, account_id: int):
        """ID로 계정을 찾는다."""
        try:
            return Account.objects.get(id=account_id)
        except ObjectDoesNotExist:
            return None

    def findByEmail(self, email: str) -> Account:
        try:
            encrypted_email = aes.encrypt(email)
            return Account.objects.get(email=encrypted_email)
        except Account.DoesNotExist:
            return None

    def updateLastUsed(self, account_id: int):
        """로그인 시 마지막 접속 날짜를 업데이트한다."""
        try:
            account = Account.objects.get(id=account_id)
            account.account_used_date = now()
            account.save()
            print(f"account_used_date 업데이트됨: {account.account_used_date}")
            return account
        except ObjectDoesNotExist:
            print(f"계정 {account_id} 찾을 수 없음음")
            return None

    def findAccountPath(self, email: str):
        try:
            account = Account.objects.get(email=email)
            return account.account_path
        except ObjectDoesNotExist:
            return None