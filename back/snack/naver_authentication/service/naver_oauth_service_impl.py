from naver_authentication.repository.naver_oauth_repository_impl import NaverOauthRepositoryImpl
from naver_authentication.service.naver_oauth_service import NaverOauthService

class NaverOauthServiceImpl(NaverOauthService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__naverOauthRepository = NaverOauthRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestNaverOauthLink(self):
        return self.__naverOauthRepository.getOauthLink()

    def requestAccessToken(self, code, state):
        return self.__naverOauthRepository.getAccessToken(code, state)

    def requestUserInfo(self, accessToken):
        return self.__naverOauthRepository.getUserInfo(accessToken)

    def requestAccessTokenForApp(self, code, state):
        return self.__naverOauthRepository.getAccessTokenForApp(code, state)
