from django.core.exceptions import ObjectDoesNotExist
from account_scrap.entity.account_scrap import AccountScrap
from account_scrap.repository.account_scrap_repository import AccountScrapRepository
from account_profile.entity.account_profile import AccountProfile
from restaurants.entity.restaurants import Restaurant

class AccountScrapRepositoryImpl(AccountScrapRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save(self, scrap: AccountScrap):
        scrap.save()
        return scrap

    def delete(self, scrap_id: int):
        try:
            scrap = AccountScrap.objects.get(id=scrap_id)
            scrap.is_deleted = True
            scrap.save()
            return True
        except ObjectDoesNotExist:
            return False

    def findByAuthor(self, author: AccountProfile):
        return AccountScrap.objects.filter(author=author, is_deleted=False)

    def findByRestaurantAndAuthor(self, restaurant: Restaurant, author: AccountProfile):
        try:
            return AccountScrap.objects.get(restaurant=restaurant, author=author, is_deleted=False)
        except ObjectDoesNotExist:
            return None