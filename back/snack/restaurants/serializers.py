from rest_framework import serializers
from restaurants.entity.restaurants import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
