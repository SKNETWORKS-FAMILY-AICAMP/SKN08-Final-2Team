import requests
from snack import settings
from naver_authentication.repository.naver_oauth_repository import NaverOauthRepository

class NaverOauthRepositoryImpl(NaverOauthRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.loginUrl = settings.NAVER['LOGIN_URL']
            cls.__instance.clientId = settings.NAVER['CLIENT_ID']
            cls.__instance.clientSecret = settings.NAVER['CLIENT_SECRET']
            cls.__instance.redirectUri = settings.NAVER['REDIRECT_URI']
            # cls.__instance.redirectUri = settings.NAVER['REDIRECT_URI_FOR_APP']
            cls.__instance.tokenRequestUri = settings.NAVER['TOKEN_REQUEST_URI']
            cls.__instance.userInfoRequestUri = settings.NAVER['USER_INFO_REQUEST_URI']

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getOauthLink(self):
        return (f"{self.loginUrl}?response_type=code"
                f"&client_id={self.clientId}&redirect_uri={self.redirectUri}&state=RANDOM_STATE")

    def getAccessToken(self, code, state):
        tokenRequest = {
            'grant_type': 'authorization_code',
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'code': code,
            'state': state
        }

        response = requests.post(self.tokenRequestUri, data=tokenRequest)
        return response.json()

    def getUserInfo(self, accessToken):
        headers = {'Authorization': f'Bearer {accessToken}'}
        response = requests.get(self.userInfoRequestUri, headers=headers)
        return response.json()


    def getAccessTokenForApp(self, code, state):
        accessTokenRequestForApp = {
            'grant_type': 'authorization_code',
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'code': code,
            'state': state
        }

        response = requests.post(self.tokenRequestUri, data=accessTokenRequestForApp)
        return response.json()
