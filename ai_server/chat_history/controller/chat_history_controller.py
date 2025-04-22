from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from chat_history.service.chat_history_service_impl import ChatHistoryServiceImpl
from chat_history.schema.chat_history_schema import ChatMessageRequest
from db import SessionLocal

chatHistoryRouter = APIRouter()


# 의존성 주입을 위한 DB 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ChatHistoryServiceImpl 의존성 주입
def injectChatHistoryService(db: Session = Depends(get_db)) -> ChatHistoryServiceImpl:
    return ChatHistoryServiceImpl(db)


@chatHistoryRouter.post("/chat-history/save")
async def save_chat_history(
    request_body: ChatMessageRequest,
    usertoken: str = Header(..., alias="userToken"),
    chatHistoryService: ChatHistoryServiceImpl = Depends(injectChatHistoryService)
):
    print("controller -> save_chat_history()")
    result = chatHistoryService.create_chat_history(
        user_token=usertoken,
        user_message=request_body.user_message,
        bot_response=request_body.bot_response
    )
    return JSONResponse(content={"message": "chat saved", "data": {
        "id": result.id,
        "user_message": result.user_message,
        "bot_response": result.bot_response,
        "timestamp": str(result.created_at)
    }})


@chatHistoryRouter.get("/chat-history/get")
async def get_chat_history(
    usertoken: str = Header(..., alias="userToken"),
    chatHistoryService: ChatHistoryServiceImpl = Depends(injectChatHistoryService)
):
    print("controller -> get_chat_history()")
    result = chatHistoryService.get_chat_history(usertoken)
    return JSONResponse(content={"history": [
        {
            "id": h.id,
            "user_message": h.user_message,
            "bot_response": h.bot_response,
            "timestamp": str(h.created_at)
        } for h in result
    ]})
