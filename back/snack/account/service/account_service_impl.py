from django.core.exceptions import ObjectDoesNotExist
from account.repository.account_repository_impl import AccountRepositoryImpl
from account.service.account_service import AccountService
from account.entity.account import Account, AccountStatus
from account.entity.account_role_type import AccountRoleType
from account.entity.role_type import RoleType
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils.timezone import now

class AccountServiceImpl(AccountService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createAccount(self, email: str, account_path: str, role_type: str) -> Account:
        """새로운 계정을 생성한다."""
        try:
            defaultRoleType = AccountRoleType.objects.get(role_type=role_type)
        except ObjectDoesNotExist:
            defaultRoleType = AccountRoleType(role_type=role_type)
            defaultRoleType.save()

        account = Account(email=email, role_type=defaultRoleType, account_path=account_path)
        return self.__accountRepository.save(account)

    def checkEmailDuplication(self, email: str) -> bool:
        """이메일 중복 확인"""
        account = self.__accountRepository.findByEmail(email)
        if account:
            return account
        return None

    def checkAccountStatus(self, account):
        """계정 상태 확인 및 처리"""
        if account is None:
            return None, None  # 계정이 존재하지 않음

        if account.account_status == 1:  # Suspended (정지된 계정)
            return None, "SUSPENDED"

        elif account.account_status == 2:  # 탈퇴 회원 (재가입 처리)
            return None, None

        elif account.account_status == 4:  # Banned (영구 정지)
            return None, "BANNED"

        return account, None  # 정상 계정 (활성)

    def findAccountById(self, account_id: int) -> Account:
        """Account ID로 계정을 찾는다."""
        return self.__accountRepository.findById(account_id)

    def updateLastUsed(self, account_id: int):
        """로그인 시 마지막 접속 날짜를 업데이트 하고 변경된 데이터를 반환한다."""
        updated_account = self.__accountRepository.updateLastUsed(account_id)
        if updated_account:
            print(f"로그인 시 account_used_date 갱신 완료: {updated_account.account_used_date}")
        else:
            print(f"계정 {account_id}를 찾을 수 없음")
        return updated_account
    
    def checkAccountPath(self, email: str, login_path: str):
        """가입된 경로와 로그인 시도 경로가 다르면 충돌 발생"""
        existing_account = self.__accountRepository.findByEmail(email)
        account_path_str = getattr(existing_account, 'account_path', 'None')

        print(f"⚡ 기존 가입된 account_path: {account_path_str}")
        print(f"🔍 checkAccountPath() - email: {email}, login_path: {login_path}")
        

        if existing_account and existing_account.account_path != login_path:
            return f"이미 {existing_account.account_path}로 가입된 이메일입니다. {login_path}로 로그인할 수 없습니다."
        return None
    
    def updateRoleToAdmin(self, account_id):
        account = Account.objects.get(id=account_id)

        # FK로 연결된 모델 인스턴스를 가져와야 함
        account.role_type = AccountRoleType.objects.get(role_type=RoleType.ADMIN)
        

        account.save()
        return True


    def deactivateAccount(self, account_id: int) -> bool:   # 휴면 계정 비활성화
        try:
            account = Account.objects.get(id=account_id)
            account.account_status = AccountStatus.SUSPENDED.value
            account.save()
            return True
        except Account.DoesNotExist:
            return False

    def deleteAccountById(self, account_id: int) -> bool:    # 휴면 계정 삭제
        try:
            account = Account.objects.get(id=account_id)
            account.delete()
            return True
        except Account.DoesNotExist:
            return False


    def suspendAccountById(self, target_account_id: int, reason: str, duration: int = None):
        """사용자 계정 정지 처리"""
        target_account = self.__accountRepository.findById(target_account_id)
        if not target_account:
            raise ValueError("대상 사용자를 찾을 수 없습니다.")


        # 정지 기간 설정
        if duration is not None:
            try:
                duration = int(duration)  # 명시적 정수 변환
                if duration <= 0:
                    raise ValueError("정지 기간은 1 이상의 정수로 지정해야 합니다.")
                suspended_until = now() + timedelta(days=duration)
            except (ValueError, TypeError):
                raise ValueError("정지 기간은 1 이상의 정수로 지정해야 합니다.")
        else:
            suspended_until = None  # 영구 정지

        # 정지 처리
        target_account.account_status = AccountStatus.SUSPENDED.value
        target_account.suspension_reason = reason
        target_account.suspended_until = suspended_until

        # 상태 저장
        self.__accountRepository.updateSuspendedAccountStatus(target_account)
        return target_account

    def isSuspended(self, account_id: int):
        """사용자 계정 정지 상태 확인"""
        #  사용자 계정 조회
        account = self.__accountRepository.findById(account_id)
        if not account:
            raise ValueError("사용자를 찾을 수 없습니다.")

        # 정지된 상태인지 확인
        if account.account_status == AccountStatus.SUSPENDED.value:
            # 정지 만료일 확인 (기간이 남아있는지)
            if account.suspended_until:
                if account.suspended_until > now():
                    # 정지된 상태 유지
                    return True, f"정지된 계정입니다. 만료일: {account.suspended_until.strftime('%Y-%m-%d %H:%M:%S')}. 사유: {account.suspension_reason}"
                else:
                    #  만료일이 지났다면 자동 정지 해제
                    account.account_status = AccountStatus.ACTIVE.value
                    account.suspended_until = None
                    account.suspension_reason = None
                    self.__accountRepository.update_account(account)
                    return False, None  # 정지 해제

            #  무기한 정지된 경우
            return True, f"무기한 정지된 계정입니다. 사유: {account.suspension_reason}"

        # 정지되지 않은 사용자 (정상)
        return False, None

    def unsuspendAccountById(self, account_id: int):
        """사용자 정지 해제"""
        account = self.__accountRepository.findById(account_id)
        if not account:
            raise ValueError("사용자를 찾을 수 없습니다.")

        if account.account_status != AccountStatus.SUSPENDED.value:
            raise ValueError("정지된 사용자만 해제할 수 있습니다.")

        # 정지 상태 해제
        account.account_status = AccountStatus.ACTIVE.value
        account.suspended_until = None
        account.suspension_reason = None

        self.__accountRepository.updateSuspendedAccountStatus(account)

    def getSuspendedAccounts(self):
        """정지된 사용자 목록 조회"""
        try:
            return self.__accountRepository.findSuspendedAccounts()
        except Exception as e:
            raise ValueError(f"정지된 사용자 목록 조회 중 오류 발생: {str(e)}")

    def banAccountById(self, target_account_id: int, reason: str):
        """사용자 계정 차단 (영구 탈퇴) 처리"""
        target_account = self.__accountRepository.findById(target_account_id)
        if not target_account:
            raise ValueError("대상 사용자를 찾을 수 없습니다.")

        # 이미 정지된 사용자인 경우에도 무시하고 바로 차단 처리
        target_account.account_status = AccountStatus.BANNED.value
        target_account.banned_reason = reason

        # 정지 상태 관련 필드 초기화
        target_account.suspended_until = None
        target_account.suspension_reason = None

        # 상태 저장 (차단 사용자)
        self.__accountRepository.updateBannedAccountStatus(target_account)
        return target_account


    def getBannedAccounts(self):
        """영구 탈퇴된 사용자 목록 조회"""
        try:
            return self.__accountRepository.findBannedAccounts()
        except Exception as e:
            raise ValueError(f"차단된 사용자 목록 조회 중 오류 발생: {str(e)}")

    def unbanAccountById(self, target_account_id: int):
        """사용자 영구탈퇴 해제"""
        target_account = self.__accountRepository.findById(target_account_id)
        if not target_account:
            raise ValueError("대상 사용자를 찾을 수 없습니다.")

        if target_account.account_status != 4:
            raise ValueError("대상 사용자가 영구탈퇴된 상태가 아닙니다.")

        # 영구탈퇴 해제
        target_account.account_status = 0  # Active 상태로 변경
        target_account.banned_reason = None  # 차단 사유 삭제
        self.__accountRepository.updateBannedAccountStatus(target_account)

