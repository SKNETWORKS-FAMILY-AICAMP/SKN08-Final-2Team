from django.urls import path
from restaurants.controller.restaurants_controller import restaurant_list

urlpatterns = [
    path('list/', restaurant_list, name="restaurant_list"),
]
