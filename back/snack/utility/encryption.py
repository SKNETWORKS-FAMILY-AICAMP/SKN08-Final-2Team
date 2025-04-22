from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from django.conf import settings

BLOCK_SIZE = 16

def pad(s):
    padding = BLOCK_SIZE - len(s.encode()) % BLOCK_SIZE
    return s + (chr(padding) * padding)

def unpad(s):
    return s[:-ord(s[-1])]

class AESCipher:
    def __init__(self):
        key = settings.ENCRYPTION_KEY  # settings에서 불러옴
        self.key = key.encode()

    def encrypt(self, raw):
        raw = pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted = cipher.encrypt(raw.encode())
        return b64encode(encrypted).decode()

    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted = cipher.decrypt(b64decode(enc))
        return unpad(decrypted.decode())

def is_encrypted(value: str) -> bool:
    try:
        AESCipher().decrypt(value)
        return True
    except:
        return False
