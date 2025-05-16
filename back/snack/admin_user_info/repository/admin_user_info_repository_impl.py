from account.entity.account import Account
from account_profile.entity.account_profile import AccountProfile
from admin_user_info.repository.admin_user_info_repository import AdminUserInfoRepository
from utility.encryption import AESCipher

aes = AESCipher()  # AES 인스턴스 생성

class AdminUserInfoRepositoryImpl(AdminUserInfoRepository):
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


    def findUserById(self, user_id):
        user = (
            Account.objects
            .select_related('accountprofile')  # AccountProfile과 조인
            .filter(id=user_id)
            .values(
                'id', 'email', 'account_status', 'account_path', 'account_register',
                'accountprofile__account_name', 'accountprofile__account_nickname',
                'accountprofile__phone_num', 'accountprofile__account_add',
                'accountprofile__account_sex', 'accountprofile__account_birth',
                'accountprofile__account_pay', 'accountprofile__account_sub'
            )
            .first()
        )
        if not user:
            return None

        return self.__formatDecryptedUserInfo(user)

    def __formatDecryptedUserInfo(self, user):
        def decrypt_field(value):
            try:
                return aes.decrypt(value) if value else ""
            except:
                return value

        return {
            "id": user['id'],
            "email": decrypt_field(user['email']),
            "account_status": user['account_status'],
            "account_path": user['account_path'],
            "created_at": user['account_register'],
            "profile": {
                "name": decrypt_field(user.get('accountprofile__account_name')),
                "nickname": user.get('accountprofile__account_nickname'),  # 닉네임은 복호화 필요 없음
                "phone_num": decrypt_field(user.get('accountprofile__phone_num')),
                "address": decrypt_field(user.get('accountprofile__account_add')),
                "gender": user.get('accountprofile__account_sex'),         # 성별은 복호화 필요 없음
                "birth": decrypt_field(user.get('accountprofile__account_birth')),
                "payment": self.__decrypt_payment(user.get('accountprofile__account_pay')),
                "subscribed": user.get('accountprofile__account_sub')      # 구독여부 복호화 필요 없음
            }
        }

    # 결제 정보 복호화 및 JSON 변환 처리
    def __decrypt_payment(self, encrypted_payment):
        try:
            import json
            decrypted_payment = aes.decrypt(encrypted_payment) if encrypted_payment else ""
            return json.loads(decrypted_payment) if decrypted_payment else {}
        except:
            return encrypted_payment

    def findAllUsersInfo(self):
        user_dict = (
            Account.objects
            .select_related('accountprofile')
            .all()
            .values(
                'id', 'email', 'account_status', 'account_path', 'account_register',
                'accountprofile__account_name', 'accountprofile__account_nickname',
                'accountprofile__phone_num', 'accountprofile__account_add',
                'accountprofile__account_sex', 'accountprofile__account_birth',
                'accountprofile__account_pay', 'accountprofile__account_sub'
            )
        )
        return [self.__formatDecryptedUserInfo(user) for user in user_dict]

