from abc import ABC, abstractmethod

class MetaOauthService(ABC):
    @abstractmethod
    def requestMetaOauthLink(self): pass

    @abstractmethod
    def requestAccessToken(self, code): pass

    @abstractmethod
    def requestUserInfo(self, accessToken): pass
