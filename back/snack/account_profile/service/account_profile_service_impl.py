from account_profile.repository.account_profile_repository_impl import AccountProfileRepositoryImpl
from account_profile.entity.account_profile import AccountProfile
from account_profile.service.account_profile_service import AccountProfileService

class AccountProfileServiceImpl(AccountProfileService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__repository = AccountProfileRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createAccountProfile(
        self, account_id: int, account_name: str, account_nickname: str, phone_num: str,
        account_add: str, account_sex: str, account_birth: str, account_pay: dict, account_sub: bool, account_age: int = None
    ) -> AccountProfile:
        """새로운 AccountProfile을 생성한다."""
        profile = AccountProfile(
            account_id=account_id, account_name=account_name, account_nickname=account_nickname,
            phone_num=phone_num, account_add=account_add, account_sex=account_sex,
            account_birth=account_birth, account_pay=account_pay, account_sub=account_sub,
            account_age=str(account_age) if account_age is not None else None,
        )
        return self.__repository.save(profile)

    def getProfileByAccountId(self, account_id: int) -> dict:
        """Account ID로 프로필을 찾는다."""
        return self.__repository.findByAccount(account_id)
    
    def updateNicknameByAccountId(self, account_id, new_nickname):
        profile = AccountProfile.objects.get(account_id=account_id)
        profile.account_nickname = new_nickname
        profile.save(update_fields=["account_nickname"])
    
    def updateProfile(self, account_id: int, update_data: dict) -> AccountProfile:
        profile = AccountProfile.objects.get(account_id=account_id)

        # Google 로그인 여부 확인
        from account.service.account_service_impl import AccountServiceImpl
        accountService = AccountServiceImpl.getInstance()
        account = accountService.findAccountById(account_id)
        is_google_user = account.account_path == "google"

        # 수정 가능 항목만 업데이트
        if "account_nickname" in update_data:
            profile.account_nickname = update_data["account_nickname"]
        if "account_add" in update_data:
            profile.account_add = update_data["account_add"]
        if "account_pay" in update_data:
            profile.account_pay = update_data["account_pay"]
        if "account_sub" in update_data:
            profile.account_sub = update_data["account_sub"]

        # Google 사용자만 수정 가능 항목
        if is_google_user:
            if "phone_num" in update_data:
                profile.phone_num = update_data["phone_num"]
            if "account_birth" in update_data:
                profile.account_birth = update_data["account_birth"]

        return self.__repository.save(profile)

