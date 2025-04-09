from rest_framework.response import Response
from rest_framework.decorators import api_view
from restaurants.entity.restaurants import Restaurant
from restaurants.serializers import RestaurantSerializer


@api_view(['GET'])
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)
