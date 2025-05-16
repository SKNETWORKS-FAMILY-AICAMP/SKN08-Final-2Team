from abc import ABC, abstractmethod

class AdminUserInfoRepository(ABC):

    @abstractmethod
    def findUserById(self, user_id):
        pass

    @abstractmethod
    def findAllUsersInfo(self):
        pass