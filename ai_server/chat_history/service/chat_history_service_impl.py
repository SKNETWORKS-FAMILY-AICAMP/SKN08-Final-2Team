# services/chat_history_service_impl.py

from sqlalchemy.orm import Session
from chat_history.entity.chat_history import ChatHistory
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl
from fastapi import HTTPException

class ChatHistoryServiceImpl:
    def __init__(self, db: Session):
        self.db = db
        self.redis = RedisCacheServiceImpl.getInstance()

    def create_chat_history(self, user_token: str, user_message: str, bot_response: str):
        account_id = self.redis.getValueByKey(user_token)
        if not account_id:
            raise HTTPException(status_code=401, detail="Invalid or expired user token.")

        history = ChatHistory(
            account_id=int(account_id),
            user_message=user_message,
            bot_response=bot_response
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def get_chat_history(self, user_token: str, limit: int = 20):
        account_id = self.redis.get_value(user_token)
        if not account_id:
            raise HTTPException(status_code=401, detail="Invalid or expired user token.")

        return (
            self.db.query(ChatHistory)
            .filter(ChatHistory.account_id == int(account_id))
            .order_by(ChatHistory.timestamp.desc())
            .limit(limit)
            .all()
        )
