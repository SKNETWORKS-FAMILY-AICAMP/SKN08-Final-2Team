import requests
from snack import settings
from google_authentication.repository.google_oauth_repository import GoogleOauthRepository

class GoogleOauthRepositoryImpl(GoogleOauthRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.loginUrl = settings.GOOGLE['LOGIN_URL']
            cls.__instance.clientId = settings.GOOGLE['CLIENT_ID']
            cls.__instance.clientSecret = settings.GOOGLE['CLIENT_SECRET']
            cls.__instance.redirectUri = settings.GOOGLE['REDIRECT_URI']
            cls.__instance.redirectUri = settings.GOOGLE['REDIRECT_URI_FOR_APP']
            cls.__instance.tokenRequestUri = settings.GOOGLE['TOKEN_REQUEST_URI']
            cls.__instance.userInfoRequestUri = settings.GOOGLE['USER_INFO_REQUEST_URI']

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def getOauthLink(self):
        return (f"{self.loginUrl}?response_type=code"
                f"&client_id={self.clientId}&redirect_uri={self.redirectUri}"
                f"&scope=email%20profile&access_type=offline&prompt=consent")

    def getAccessToken(self, code):
        tokenRequest = {
            'grant_type': 'authorization_code',
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'code': code,
            'redirect_uri': self.redirectUri,
        }

        response = requests.post(self.tokenRequestUri, data=tokenRequest)
        return response.json()

    def getUserInfo(self, accessToken):
        headers = {'Authorization': f'Bearer {accessToken}'}
        response = requests.get(self.userInfoRequestUri, headers=headers)
        return response.json()