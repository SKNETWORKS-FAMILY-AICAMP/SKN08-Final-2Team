from chat_history.entity.chat_history import ChatHistory
from chat_history.repository.chat_history_repository_impl import ChatHistoryRepositoryImpl
from account_profile.entity.account_profile import AccountProfile
from typing import List, Dict


class ChatHistoryServiceImpl:
    __repository = ChatHistoryRepositoryImpl()

    def saveChatHistory(self, author: AccountProfile, user_message: str, bot_response: str) -> None:
        self.__repository.save(author, user_message, bot_response)

    def getAllChatHistory(self, author: AccountProfile) -> Dict[str, List[str]]:
        history = self.__repository.getAll(author)
        user_messages = [record.user_message for record in history]
        bot_responses = [record.bot_response for record in history]
        return {"user_messages": user_messages, "bot_responses": bot_responses}

    def getRecentChatHistory(self, author: AccountProfile) -> List[Dict[str, str]]:
        history = self.__repository.getRecent(author, limit=15)
        return [
            {
                "user_message": record.user_message,
                "bot_response": record.bot_response,
                "created_at": record.getCreatedAt()
            }
            for record in history
        ]
