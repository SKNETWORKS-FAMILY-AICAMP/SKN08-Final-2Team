from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view
from restaurants.entity.restaurants import Restaurant
from restaurants.serializers import RestaurantSerializer


@api_view(['GET'])
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)


from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from restaurants.entity.restaurants import Restaurant
from restaurants.serializers import RestaurantSerializer

# @api_view(['GET'])
# def restaurant_search(request):
#     keyword = request.GET.get('keyword', '')
#     if not keyword:
#         return Response([])

#     # ✅ 공백 기준으로 다중 키워드 분리
#     keywords = keyword.strip().split()

#     # ✅ 다중 Q 조건을 OR로 결합
#     query = Q()
#     for word in keywords:
#         query |= Q(name__icontains=word)
#         query |= Q(category__icontains=word)
#         query |= Q(address__icontains=word)

#     queryset = Restaurant.objects.filter(query).distinct()
#     serializer = RestaurantSerializer(queryset, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
def restaurant_search(request):
    keyword = request.GET.get('keyword', '')
    if not keyword:
        return Response([])

    keywords = keyword.strip().split()

    query = Q()
    for word in keywords:
        word_query = (
            Q(name__icontains=word) |
            Q(category__icontains=word) |
            Q(address__icontains=word) |
            Q(keyword__icontains=word)  # ✅ keyword 필드 추가
        )
        query &= word_query  # ✅ AND 조건으로 누적

    queryset = Restaurant.objects.filter(query).distinct()
    serializer = RestaurantSerializer(queryset, many=True)
    return Response(serializer.data)
