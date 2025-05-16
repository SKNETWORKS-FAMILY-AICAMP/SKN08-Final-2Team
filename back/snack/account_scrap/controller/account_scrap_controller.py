from rest_framework import viewsets, status
from django.http import JsonResponse
from account_scrap.service.account_scrap_service_impl import AccountScrapServiceImpl
from account_profile.entity.account_profile import AccountProfile
from restaurants.entity.restaurants import Restaurant
from account.service.account_service_impl import AccountServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl

class AccountScrapController(viewsets.ViewSet):
    __scrapService = AccountScrapServiceImpl.getInstance()
    __redisService = RedisCacheServiceImpl.getInstance()

    def createScrap(self, request):
        userToken = request.headers.get("Authorization", "").replace("Bearer ", "")
        account_id = self.__redisService.getValueByKey(userToken)

        if not account_id:
            return JsonResponse({"error": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        author = AccountProfile.objects.get(account__id=account_id)
        restaurant_id = request.data.get("restaurant_id")

        if not restaurant_id:
            return JsonResponse({"error": "식당 정보가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        restaurant = Restaurant.objects.get(id=restaurant_id)
        scrap = self.__scrapService.createScrap(author, restaurant)

        return JsonResponse({"success": True, "scrap_id": scrap.id}, status=status.HTTP_201_CREATED)

    def deleteScrap(self, request, scrap_id):
        success = self.__scrapService.deleteScrap(scrap_id)
        return JsonResponse({"success": success}, status=status.HTTP_200_OK if success else status.HTTP_404_NOT_FOUND)

    def getMyScraps(self, request):
        userToken = request.headers.get("Authorization", "").replace("Bearer ", "")
        account_id = self.__redisService.getValueByKey(userToken)

        if not account_id:
            return JsonResponse({"error": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        author = AccountProfile.objects.get(account__id=account_id)
        scraps = self.__scrapService.getScrapsByAuthor(author)

        return JsonResponse({
            "success": True,
            "scraps": [
                {
                    "scrap_id": s.id,
                    "restaurant_id": s.restaurant.id,
                    "restaurant_name": s.restaurant.name,
                    "created_at": s.created_at
                } for s in scraps
            ]
        }, status=status.HTTP_200_OK)