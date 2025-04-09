import requests

from db_automation import settings
from github_action_monitor.repository.github_action_monitor_repository import GithubActionMonitorRepository
from utility.http_client import HttpClient


class GithubActionMonitorRepositoryImpl(GithubActionMonitorRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getGithubActionWorkflow(self, token: str, repoUrl: str):
        """Fiber 서버에 요청하여 GitHub Actions Workflow 상태 가져오기"""
        endpoint = "/github-actions/workflow"  # 엔드포인트 수정
        data = {"token": token, "repo_url": repoUrl}
        print(f"token: {token}, repoUrl: {repoUrl}")

        try:
            # HttpClient의 비동기 POST 메서드를 사용하여 요청
            result = HttpClient.post(endpoint, data)

            if result:
                print(f"✅ 성공: GitHub Workflow 데이터 수신")
                return result  # 응답을 그대로 반환
            else:
                print(f"❌ 오류: 요청 실패")
                return None

        except Exception as e:
            print(f"⚠️ 요청 실패: {str(e)}")
            return None
