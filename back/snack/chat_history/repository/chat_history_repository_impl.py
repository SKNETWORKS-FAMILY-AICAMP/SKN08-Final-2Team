from chat_history.entity.chat_history import ChatHistory
from account_profile.entity.account_profile import AccountProfile
from chat_history.repository.chat_history_repository import ChatHistoryRepository

class ChatHistoryRepositoryImpl(ChatHistoryRepository):
    def save(self, author: AccountProfile, user_message: str, bot_response: str) -> None:
        ChatHistory.objects.create(
            author=author,
            user_message=user_message,
            bot_response=bot_response
        )

    def getAll(self, author: AccountProfile):
        return ChatHistory.objects.filter(author=author).order_by('-created_at')

    def getRecent(self, author: AccountProfile, limit: int = 15):
        return ChatHistory.objects.filter(author=author).order_by('-created_at')[:limit]
