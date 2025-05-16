from account_scrap.service.account_scrap_service import AccountScrapService
from account_scrap.repository.account_scrap_repository_impl import AccountScrapRepositoryImpl
from account_scrap.entity.account_scrap import AccountScrap
from account_profile.entity.account_profile import AccountProfile
from restaurants.entity.restaurants import Restaurant

class AccountScrapServiceImpl(AccountScrapService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__scrapRepository = AccountScrapRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createScrap(self, author: AccountProfile, restaurant: Restaurant) -> AccountScrap:
        existing = self.__scrapRepository.findByRestaurantAndAuthor(restaurant, author)
        if existing:
            return existing  # 이미 스크랩한 경우는 기존 반환
        scrap = AccountScrap(restaurant=restaurant, author=author)
        return self.__scrapRepository.save(scrap)

    def deleteScrap(self, scrap_id: int) -> bool:
        return self.__scrapRepository.delete(scrap_id)

    def getScrapsByAuthor(self, author: AccountProfile):
        return self.__scrapRepository.findByAuthor(author)