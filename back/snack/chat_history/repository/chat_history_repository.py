from chat_history.entity.chat_history import ChatHistory
from account_profile.entity.account_profile import AccountProfile
from typing import List
from abc import ABC, abstractmethod


class ChatHistoryRepository(ABC):
    @abstractmethod
    def save(self, author: AccountProfile, user_message: str, bot_response: str) -> None:
        pass

    @abstractmethod
    def getAll(self, author: AccountProfile) -> List[ChatHistory]:
        pass

    @abstractmethod
    def getRecent(self, author: AccountProfile, limit: int = 15) -> List[ChatHistory]:
        pass
