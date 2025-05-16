from admin_user_info.repository.admin_user_info_repository_impl import AdminUserInfoRepositoryImpl
from admin_user_info.service.admin_user_info_service import AdminUserInfoService


class AdminUserInfoServiceImpl(AdminUserInfoService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__accountRepository = AdminUserInfoRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def getUserInfo(self, user_id):
        return self.__accountRepository.findUserById(user_id)


    def getUserInfoList(self):
        return self.__accountRepository.findAllUsersInfo()