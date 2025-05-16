from abc import ABC, abstractmethod
from account_scrap.entity.account_scrap import AccountScrap
from account_profile.entity.account_profile import AccountProfile
from restaurants.entity.restaurants import Restaurant

class AccountScrapRepository(ABC):
    @abstractmethod
    def save(self, scrap: AccountScrap):
        pass

    @abstractmethod
    def delete(self, scrap_id: int):
        pass

    @abstractmethod
    def findByAuthor(self, author: AccountProfile):
        pass

    @abstractmethod
    def findByRestaurantAndAuthor(self, restaurant: Restaurant, author: AccountProfile):
        pass
