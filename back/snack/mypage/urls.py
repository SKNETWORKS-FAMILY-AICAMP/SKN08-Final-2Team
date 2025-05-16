from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mypage.controller.mypage_controller import MypageController

router = DefaultRouter()
router.register(r"mypage", AccountController, basename='mypage')

urlpatterns = [
    path("", include(router.urls)),
]