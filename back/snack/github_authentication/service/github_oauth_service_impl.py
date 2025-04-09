from github_authentication.repository.github_oauth_repository_impl import GithubOauthRepositoryImpl
from github_authentication.service.github_oauth_service import GithubOauthService

import os

class GithubOauthServiceImpl(GithubOauthService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__githubOauthRepository = GithubOauthRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestGithubOauthLink(self):
        return self.__githubOauthRepository.getOauthLink()

    def requestAccessToken(self, code):
        print("✅ GITHUB_REDIRECT_URI:", os.getenv("GITHUB_REDIRECT_URI"))
        print("✅ GITHUB_CLIENT_ID:", os.getenv("GITHUB_CLIENT_ID"))

        return self.__githubOauthRepository.getAccessToken(code)

    def requestUserInfo(self, accessToken):
        return self.__githubOauthRepository.getUserInfo(accessToken)

    def validateAdminCode(self, adminCode: str) -> bool:
        print(f"service - validateAdminCode: {adminCode}")
        return self.__githubOauthRepository.getAdminCode(adminCode)
    