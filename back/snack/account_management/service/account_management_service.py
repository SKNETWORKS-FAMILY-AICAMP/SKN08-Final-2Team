from abc import ABC, abstractmethod

class AccountManagementService:

    @abstractmethod
    def deleteExpiredAccounts(self):
        pass

    # @abstractmethod
    # def deleteExpiredAccounts(self):
    #     pass
