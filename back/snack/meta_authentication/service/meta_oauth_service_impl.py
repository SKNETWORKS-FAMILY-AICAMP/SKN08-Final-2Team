from meta_authentication.repository.meta_oauth_repository_impl import MetaOauthRepositoryImpl
from meta_authentication.service.meta_oauth_service import MetaOauthService

class MetaOauthServiceImpl(MetaOauthService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__metaOauthRepository = MetaOauthRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def requestMetaOauthLink(self):
        return self.__metaOauthRepository.getOauthLink()

    def requestAccessToken(self, code):
        return self.__metaOauthRepository.getAccessToken(code)

    def requestUserInfo(self, accessToken):
        return self.__metaOauthRepository.getUserInfo(accessToken)
