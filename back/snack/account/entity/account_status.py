from enum import Enum

class AccountStatus(Enum):
    ACTIVE = 0     # 횔성 상태
    SUSPENDED = 1  # 사용 정지
    DELETED = 2    # 회원 탈퇴
    BANNED = 4     # 영구 정지
