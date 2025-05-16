from django.urls import path
from rest_framework.routers import DefaultRouter
from chat_history.controller.chat_history_controller import ChatHistoryController

# DRF Router 설정
router = DefaultRouter()
router.register(r'chat-history', ChatHistoryController, basename='chat-history')

urlpatterns = [
    path('save', ChatHistoryController.as_view({'post': 'saveChatHistory'}), name='save-chat-history'),
    path('list', ChatHistoryController.as_view({'get': 'getChatHistory'}), name='list-chat-history'),
    path('recent', ChatHistoryController.as_view({'get': 'recentChatHistory'}), name='recent-chat-history'),
]

# DRF router의 URL을 포함
urlpatterns += router.urls
