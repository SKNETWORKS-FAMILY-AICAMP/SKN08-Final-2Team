from abc import ABC, abstractmethod

class AdminUserInfoService(ABC):

    @abstractmethod
    def getUserInfo(self, user_id):
        pass

    @abstractmethod
    def getUserInfoList(self):
        pass