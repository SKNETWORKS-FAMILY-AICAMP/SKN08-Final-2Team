from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatHistoryCreate(BaseModel):
    user_id: str
    message: str
    response: str

class ChatHistoryOut(ChatHistoryCreate):
    created_at: datetime

class ChatMessageRequest(BaseModel):
    user_message: str
    bot_response: str