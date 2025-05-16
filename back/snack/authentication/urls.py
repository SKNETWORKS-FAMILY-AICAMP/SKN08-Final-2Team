from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authentication.controller.authentication_controller import AuthenticationController

router = DefaultRouter()
router.register(r"authentication", AuthenticationController, basename='authentication')

urlpatterns = [
    path('kakao-logout', AuthenticationController.as_view({ 'post': 'requestKakaoLogout' }),
         name='request-kakao-logout'),
    path('naver-logout', AuthenticationController.as_view({ 'post': 'requestNaverLogout' }),
         name='request-naver-logout'),
    path('google-logout', AuthenticationController.as_view({'post': 'requestGoogleLogout'}),
         name='request-google-logout'),
    path('github-logout', AuthenticationController.as_view({'post': 'requestGithubLogout'}),
         name='request-github-logout'),
    path('validation', AuthenticationController.as_view({ 'post': 'requestUserTokenValidation' }),
         name='유저 토큰 유효성 검증 요청'),

    path('', include(router.urls)),
]