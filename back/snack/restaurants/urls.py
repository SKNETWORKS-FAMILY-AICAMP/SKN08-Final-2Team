from django.urls import path
from restaurants.controller.restaurants_controller import restaurant_list, restaurant_search

urlpatterns = [
    path('list', restaurant_list, name="restaurant_list"),
    path('search', restaurant_search, name="restaurant_search")
]
