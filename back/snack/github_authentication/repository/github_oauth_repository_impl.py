import uuid
import requests

from snack import settings
from github_authentication.repository.github_oauth_repository import GithubOauthRepository


class GithubOauthRepositoryImpl(GithubOauthRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.loginUrl = settings.GITHUB['LOGIN_URL']
            cls.__instance.clientId = settings.GITHUB['CLIENT_ID']
            cls.__instance.clientSecret = settings.GITHUB['CLIENT_SECRET']
            cls.__instance.redirectUri = settings.GITHUB['REDIRECT_URI']
            cls.__instance.tokenRequestUri = settings.GITHUB['TOKEN_REQUEST_URI']
            cls.__instance.userInfoRequestUri = settings.GITHUB['USER_INFO_REQUEST_URI']
            cls.__instance.adminCode = settings.GITHUB['ADMIN_CODE']
            cls.__instance.scope = settings.GITHUB['SCOPE']

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getOauthLink(self):
        print("getOauthLink() for Login")

        return (f"{self.loginUrl}?"
                f"client_id={self.clientId}"
                f"&redirect_uri={self.redirectUri}"
                f"&scope={self.scope}")

    def getAccessToken(self, githubAuthCode):
        print(f"getAccessToken(): {githubAuthCode}")

        accessTokenRequestForm = {
            "client_id": self.clientId,
            "client_secret": self.clientSecret,
            "code": githubAuthCode,
            "redirect_uri": self.redirectUri
        }
        headers = {
            "Accept": "application/json"
        }

        print(f"accessTokenRequestForm: {accessTokenRequestForm}")
        print(f"tokenRequestUri: {self.tokenRequestUri}")

        response = requests.post(self.tokenRequestUri, data=accessTokenRequestForm, headers=headers)
        return response.json()

    def getUserInfo(self, accessToken):
        headers = {
            'Authorization': f'token {accessToken}',
            'Accept': 'application/vnd.github.v3+json'
        }

        # 1차 기본 유저 정보 요청
        user_info_resp = requests.get("https://api.github.com/user", headers=headers)
        user_info_resp.raise_for_status()
        user_info = user_info_resp.json()

        print("🧾 기본 유저 정보:", user_info)

        # 이메일 보완 처리
        if not user_info.get("email"):
            try:
                email_resp = requests.get("https://api.github.com/user/emails", headers=headers)
                email_resp.raise_for_status()
                email_list = email_resp.json()
                print("📬 이메일 목록:", email_list)

                for e in email_list:
                    if e.get("primary") and e.get("verified"):
                        user_info["email"] = e["email"]
                        break

            except Exception as e:
                print("⚠️ 이메일 정보 가져오기 실패, fallback 이메일 사용:", e)
                # fallback 이메일
                login = user_info.get("login", f"unknown{uuid.uuid4().hex[:4]}")
                user_info["email"] = f"{login}@users.noreply.github.com"

        return user_info



    def getAdminCode(self, adminCode: str) -> bool:
        print(f"repository validateAdminCode adminCode: {adminCode}")
        print(f"repository validateAdminCode self.adminCode: {self.adminCode}")

        if self.adminCode is None:
            raise ValueError("GITHUB_ADMIN_CODE is not set in settings.")

        return adminCode == self.adminCode
