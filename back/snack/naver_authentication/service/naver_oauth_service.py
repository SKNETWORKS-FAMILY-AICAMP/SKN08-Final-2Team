from abc import ABC, abstractmethod

class NaverOauthService(ABC):

    @abstractmethod
    def requestNaverOauthLink(self):
        pass

    @abstractmethod
    def requestAccessToken(self, code, state):
        pass

    @abstractmethod
    def requestUserInfo(self, accessToken):
        pass

    @abstractmethod
    def requestAccessTokenForApp(self, code, state):
        pass
