from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from account_profile.entity.account_profile import AccountProfile
from account_profile.repository.account_profile_repository import AccountProfileRepository
from utility.encryption import AESCipher

aes = AESCipher()

class AccountProfileRepositoryImpl(AccountProfileRepository):
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

    def save(self, account_profile: AccountProfile):
        account_profile.save()
        return account_profile

    def findByAccount(self, account_id: int):
        try:
            profile = AccountProfile.objects.get(account_id=account_id)

            # 복호화 시도 (실패해도 무시)
            try:
                name = aes.decrypt(profile.account_name) if profile.account_name else ""
            except:
                name = profile.account_name

            try:
                phone = aes.decrypt(profile.phone_num) if profile.phone_num else ""
            except:
                phone = profile.phone_num

            try:
                address = aes.decrypt(profile.account_add) if profile.account_add else ""
            except:
                address = profile.account_add

            try:
                birth = aes.decrypt(profile.account_birth) if profile.account_birth else ""
            except:
                birth = profile.account_birth

            try:
                age = aes.decrypt(profile.account_age) if profile.account_age else ""
            except:
                age = profile.account_age

            try:
                import json
                pay = aes.decrypt(profile.account_pay) if profile.account_pay else {}
                pay = json.loads(pay) if isinstance(pay, str) else pay
            except:
                pay = profile.account_pay

            return {
                "account_id": profile.account.id,
                "account_name": name,
                "account_nickname": profile.account_nickname,
                "phone_num": phone,
                "account_add": address,
                "account_sex": profile.account_sex,
                "account_birth": birth,
                "account_age": age,
                "account_pay": pay,
                "account_sub": profile.account_sub,
                "alarm_board_status": profile.alarm_board_status,
                "alarm_comment_status": profile.alarm_comment_status
            }

        except ObjectDoesNotExist:
            return None

    def findByNickname(self, account_nickname: str):
        try:
            return AccountProfile.objects.get(account_nickname=account_nickname)
        except AccountProfile.DoesNotExist:
            return None
