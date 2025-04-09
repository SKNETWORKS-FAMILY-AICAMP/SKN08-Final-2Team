import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class HttpClient:
    _client = None  # Singleton 관리

    @classmethod
    def getClient(cls):
        """httpx.Client 싱글톤 객체 반환 (동기)"""
        if cls._client is None:
            cls._client = httpx.Client(
                base_url=os.getenv("FIBER_URL"),
                timeout=25  # 초 단위
            )
        return cls._client

    @classmethod
    def post(cls, endpoint: str, data: dict) -> bool:
        """Fiber 서버에 동기 POST 요청을 보냄"""
        client = cls.getClient()

        try:
            response = client.post(endpoint, json=data)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to send request to Fiber: {response.status_code}")
                return False

        except httpx.RequestError as exc:
            print(f"⚠️ An error occurred while sending request to Fiber: {str(exc)}")
            return False

    @classmethod
    def close(cls):
        """httpx.Client 종료"""
        if cls._client:
            cls._client.close()
            cls._client = None  # 객체 초기화