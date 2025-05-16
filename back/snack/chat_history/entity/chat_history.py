from django.db import models
from account_profile.entity.account_profile import AccountProfile
from datetime import datetime

class ChatHistory(models.Model):
    author = models.ForeignKey(AccountProfile, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 자동 생성 시간 기록

    class Meta:
        ordering = ['-created_at']
        db_table = 'chat_history'
        app_label = 'chat_history'

    def getCreatedAt(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')
