from fastapi import APIRouter, Request, Depends, Header
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy.orm import Session
from db import get_db  # db.py에 정의된 get_db import
from llm.service.llm_service_impl import LLMServiceImpl
from chat_history.service.chat_history_service_impl import ChatHistoryServiceImpl
from llm.service.prompt_builder import PromptBuilder
from weather.service.weather_service_impl import WeatherServiceImpl
from llm.entity.connect_account_prefer import AccountPrefer

llmRouter = APIRouter()

async def injectLLMService() -> LLMServiceImpl:
    return LLMServiceImpl()

def injectChatHistoryService(db: Session = Depends(get_db)) -> ChatHistoryServiceImpl:
    return ChatHistoryServiceImpl(db)

@llmRouter.post("/llm/search")
async def search_llm(
    request: Request,
    db: Session = Depends(get_db),
    usertoken: str = Header(...),
    account_id: str = Header(...),
    llmService: LLMServiceImpl = Depends(injectLLMService),
):
    print(usertoken)
    data = await request.json()
    query = data.get("query")
    print(account_id)

    if not query or not account_id:
        return JSONResponse(status_code=400, content={"message": "query/account_id 누락"})

    prefer = db.query(AccountPrefer).filter_by(account_id=account_id).first()
    if not prefer:
        return JSONResponse(status_code=404, content={"message": "선호 정보 없음"})

    weather = WeatherServiceImpl().get_seoul_weather()

    builder = PromptBuilder(prefer_model=prefer, weather=weather)
    prompt = builder.build_prompt(query)

    answer = llmService.get_response_from_openai(prompt)

    return JSONResponse(content={"response": answer})
