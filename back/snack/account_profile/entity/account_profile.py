from django.db import models
from account.entity.account import Account
from django.utils.timezone import now
from datetime import date,datetime
from utility.encryption import AESCipher, is_encrypted
aes = AESCipher()

class AccountProfile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)  # FK + PK
    account_name = models.CharField(max_length=100,null=True, blank=True)  # 사용자 이름 (수정 불가)
    account_nickname = models.CharField(max_length=100,null=True, blank=True)  # 닉네임 (수정 가능)
    phone_num = models.CharField(max_length=255, null=True, blank=True)  # 핸드폰 번호 (수정 가능)
    account_add = models.CharField(max_length=255, null=True, blank=True)  # 주소 (수정 가능)
    account_sex = models.CharField(
        max_length=10,
        choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')],
        null=True,
        blank=True
    )  # 성별 (수정 불가)
    account_birth = models.CharField(max_length=100,null=True, blank=True)  # 생년월일 (수정 불가)
    account_pay = models.JSONField(null=True, blank=True)  # 결제 정보 (수정 가능)
    account_sub = models.BooleanField(default=False)  # 구독 여부 (수정 가능)
    account_age = models.CharField(max_length=100,null=True, blank=True)
    alarm_board_status = models.BooleanField(default=True)  # 댓글 알림 허용 디폴트
    alarm_comment_status = models.BooleanField(default=True)  # 대댓글 알림 허용 디폴트

    class Meta:
        db_table = 'account_profile'
        app_label = 'account_profile'

    def __str__(self):
        return f"{self.account_nickname} - 가입일: {self.account.account_register.strftime('%Y-%m-%d')}"

    def get_age(self):
        from utility.encryption import AESCipher
        aes = AESCipher()
        try:
            decrypted_birth = aes.decrypt(self.account_birth)
        except Exception as e:
            print(f"[get_age] 복호화 실패: {e}, 원본값: {self.account_birth}")
            return None  # 복호화 실패 시 None 리턴

        try:
            birth_date = datetime.strptime(decrypted_birth, "%Y-%m-%d").date()
            today = date.today()
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        except Exception as e:
            print(f"[get_age] 생일 파싱 실패: {e}, 값: {decrypted_birth}")
            return None

    def get_role(self):
        return self.account.role_type.role_type
    
    def save(self, *args, **kwargs):

        if self.account_birth:
            try:
                decrypted_birth = aes.decrypt(self.account_birth) if is_encrypted(self.account_birth) else self.account_birth
                birth_date = datetime.strptime(decrypted_birth, "%Y-%m-%d").date()
                today = date.today()
                calculated_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                self.account_age = str(calculated_age)
            except Exception as e:
                print(f"[save] 생일 복호화 또는 나이 계산 실패: {e}")
                self.account_age = None

        if self.account_name:
            try:
                aes.decrypt(self.account_name)  # 복호화 가능하면 이미 암호화된 것
            except:
                self.account_name = aes.encrypt(self.account_name)

        if self.phone_num:
            try:
                aes.decrypt(self.phone_num)
            except:
                self.phone_num = aes.encrypt(self.phone_num)

        if self.account_add:
            try:
                aes.decrypt(self.account_add)
            except:
                self.account_add = aes.encrypt(self.account_add)

        if self.account_birth:
            try:
                aes.decrypt(self.account_birth)
            except:
                self.account_birth = aes.encrypt(str(self.account_birth))

        if self.account_pay:
            import json
            try:
                aes.decrypt(self.account_pay)
            except:
                self.account_pay = aes.encrypt(json.dumps(self.account_pay))

        super().save(*args, **kwargs)
