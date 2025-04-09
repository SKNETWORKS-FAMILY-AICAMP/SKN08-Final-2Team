from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication.controller.authentication_controller import AuthenticationController

router = DefaultRouter()
router.register(r"authentication", AuthenticationController, basename='authentication')

urlpatterns = [
    path('', include(router.urls)),
    path('kakao-logout',
         AuthenticationController.as_view({ 'post': 'requestKakaoLogout' }),
         name='로그아웃 요청'),
    path('naver-logout',
         AuthenticationController.as_view({ 'post': 'requestNaverLogout' }),
         name='로그아웃 요청'),
    path('validation',
         AuthenticationController.as_view({ 'post': 'requestUserTokenValidation' }),
         name='유저 토큰 유효성 검증 요청'),
]