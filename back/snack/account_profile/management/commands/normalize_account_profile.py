from django.core.management.base import BaseCommand
from account_profile.entity.account_profile import AccountProfile
from utility.encryption import AESCipher
from datetime import datetime
import json


aes = AESCipher()

def decrypt_until_plain(ciphertext, is_date=False, is_number=False):
    current = ciphertext
    for depth in range(60):  # 최대 5단계 복호화 시도
        try:
            decrypted = aes.decrypt(current)

            if is_date:
                try:
                    datetime.strptime(decrypted, "%Y-%m-%d")
                    return decrypted
                except:
                    pass
            elif is_number:
                if decrypted.isdigit():
                    return decrypted
            else:
                if any(char.isalpha() for char in decrypted):
                    return decrypted

            current = decrypted
        except Exception:
            break
    return None


class Command(BaseCommand):
    help = "Normalize encrypted AccountProfile fields"

    def handle(self, *args, **kwargs):
        for profile in AccountProfile.objects.all():
            changed = False

            # 이름
            if profile.account_name:
                plain = decrypt_until_plain(profile.account_name)
                if plain:
                    profile.account_name = aes.encrypt(plain)
                    changed = True
                else:
                    self.stdout.write(f"[!] 이름 복호화 실패: {profile.account_name}")

            # 전화번호
            if profile.phone_num:
                plain = decrypt_until_plain(profile.phone_num, is_number=True)
                if plain:
                    profile.phone_num = aes.encrypt(plain)
                    changed = True
                else:
                    self.stdout.write(f"[!] 전화번호 복호화 실패: {profile.phone_num}")

            # 주소
            if profile.account_add:
                plain = decrypt_until_plain(profile.account_add)
                if plain:
                    profile.account_add = aes.encrypt(plain)
                    changed = True
                else:
                    self.stdout.write(f"[!] 주소 복호화 실패: {profile.account_add}")

            # 생일
            if profile.account_birth:
                plain = decrypt_until_plain(profile.account_birth, is_date=True)
                if plain:
                    profile.account_birth = aes.encrypt(plain)
                    changed = True
                else:
                    self.stdout.write(f"[!] 생일 복호화 실패: {profile.account_birth}")

            # 나이
            if profile.account_age:
                plain = decrypt_until_plain(profile.account_age, is_number=True)
                if plain:
                    profile.account_age = aes.encrypt(plain)
                    changed = True
                else:
                    self.stdout.write(f"[!] 나이 복호화 실패: {profile.account_age}")

            # 결제 정보
            if profile.account_pay:
                try:
                    decrypted = aes.decrypt(profile.account_pay)
                    for _ in range(5):
                        if decrypted.startswith("{"):
                            json.loads(decrypted)
                            profile.account_pay = aes.encrypt(decrypted)
                            changed = True
                            break
                        decrypted = aes.decrypt(decrypted)
                except:
                    self.stdout.write("[!] 결제정보 복호화 실패")

            if changed:
                profile.save()
                self.stdout.write(f"✅ {profile.account_id} 정리 완료")
