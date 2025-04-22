from django.urls import path, include
from rest_framework.routers import DefaultRouter

from meta_authentication.controller.meta_oauth_controller import MetaOauthController
router = DefaultRouter()
router.register(r"meta-oauth", MetaOauthController, basename='naver-oauth')

urlpatterns = [
    path('', include(router.urls)),
    path('request-login-url',
         MetaOauthController.as_view({ 'get': 'requestMetaOauthLink' }),
         name='naver Oauth 링크 요청'),
    path('redirect-access-token',
         MetaOauthController.as_view({ 'get': 'requestAccessToken','post': 'requestAccessToken' }),
         name='naver Access Token 요청'),
     path('request-user-token',
         MetaOauthController.as_view({ 'post': 'requestUserToken' }),
         name='User Token 요청'),
]