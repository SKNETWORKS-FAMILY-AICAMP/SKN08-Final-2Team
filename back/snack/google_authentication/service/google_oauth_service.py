from abc import ABC, abstractmethod

class GoogleOauthService(ABC):

    @abstractmethod
    def requestGoogleOauthLink(self):
        pass

    @abstractmethod
    def requestAccessToken(self, code):
        pass

    @abstractmethod
    def requestUserInfo(self, accessToken):
        pass
