import requests
from snack import settings
from meta_authentication.repository.meta_oauth_repository import MetaOauthRepository

class MetaOauthRepositoryImpl(MetaOauthRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.loginUrl = settings.META['LOGIN_URL']
            cls.__instance.clientId = settings.META['CLIENT_ID']
            cls.__instance.clientSecret = settings.META['CLIENT_SECRET']
            cls.__instance.redirectUri = settings.META['REDIRECT_URI']
            cls.__instance.tokenRequestUri = settings.META['TOKEN_REQUEST_URI']
            cls.__instance.userInfoRequestUri = settings.META['USER_INFO_REQUEST_URI']

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def getOauthLink(self):
        return (
            f"{self.loginUrl}?client_id={self.clientId}"
            f"&redirect_uri={self.redirectUri}"
            f"&scope=email,public_profile"
        )

    def getAccessToken(self, code):
        tokenRequest = {
            'client_id': self.clientId,
            'redirect_uri': self.redirectUri,
            'client_secret': self.clientSecret,
            'code': code
        }

        response = requests.get(self.tokenRequestUri, params=tokenRequest)
        return response.json()

    def getUserInfo(self, accessToken):
        fields = 'id,name,email,picture'
        params = {'fields': fields, 'access_token': accessToken}
        response = requests.get(self.userInfoRequestUri, params=params)
        return response.json()
