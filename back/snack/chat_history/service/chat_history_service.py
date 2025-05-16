from account_profile.entity.account_profile import AccountProfile
from typing import List, Dict
from abc import ABC, abstractmethod


class ChatHistoryService(ABC):
    @abstractmethod
    def saveChatHistory(self, author: AccountProfile, user_message: str, bot_response: str) -> None:
        pass

    @abstractmethod
    def getAllChatHistory(self, author: AccountProfile) -> Dict[str, List[str]]:
        pass

    @abstractmethod
    def getRecentChatHistory(self, author: AccountProfile) -> List[Dict[str, str]]:
        pass
