from abc import ABC, abstractmethod
from account_scrap.entity.account_scrap import AccountScrap
from account_profile.entity.account_profile import AccountProfile
from restaurants.entity.restaurants import Restaurant

class AccountScrapService(ABC):
    @abstractmethod
    def createScrap(self, author: AccountProfile, restaurant: Restaurant) -> AccountScrap:
        pass

    @abstractmethod
    def deleteScrap(self, scrap_id: int) -> bool:
        pass

    @abstractmethod
    def getScrapsByAuthor(self, author: AccountProfile):
        pass
