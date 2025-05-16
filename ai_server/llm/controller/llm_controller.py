# llm_controller.py
from fastapi import APIRouter, Request, Depends, Header
from fastapi.responses import StreamingResponse
from llm.service.llm_service_impl import LLMServiceImpl
from llm.service.prompt_builder import PromptBuilder
from weather.service.weather_service_impl import WeatherServiceImpl
import requests
import os

llmRouter = APIRouter()

def fetch_user_preference(account_id):
    base_url = os.getenv("DJANGO_BASE_URL", "http://localhost:8000")
    url = f"{base_url}/account-prefer/{account_id}"
    print(f"[DEBUG] 요청 URL: {url}")
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

@llmRouter.post("/llm/search")
async def search_llm(
    request: Request,
    usertoken: str = Header(...),
    account_id: str = Header(...),
    llmService: LLMServiceImpl = Depends(LLMServiceImpl),
):
    data = await request.json()
    query = data.get("query")

    if not query or not account_id:
        return StreamingResponse(
            content=iter(["[오류] query 또는 account_id가 누락되었습니다."]),
            media_type="text/plain"
        )

    prefer = fetch_user_preference(account_id)
    if not prefer:
        print(f"[경고] account_id={account_id}의 선호도 정보 없음 — 기본 프롬프트로 진행")
        prefer = {}

    weather = WeatherServiceImpl().get_seoul_weather()
    builder = PromptBuilder(prefer_model=prefer, weather=weather)
    prompt = builder.build_prompt(query)

    stream = llmService.get_streaming_openai_response(prompt)

    def generate():
        for chunk in stream:
            try:
                yield chunk.content
            except Exception as e:
                print(f"❌ 스트리밍 처리 중 오류: {e}")
                continue

    return StreamingResponse(generate(), media_type="text/plain")
