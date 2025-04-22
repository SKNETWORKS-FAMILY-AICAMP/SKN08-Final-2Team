from django.db import models
from django.utils.timezone import now, localtime
from board.entity.board import Board
from account_profile.entity.account_profile import AccountProfile
from django.utils.timezone import localtime, is_aware, make_aware

class Comment(models.Model):
    id = models.AutoField(primary_key=True)  # 댓글 ID
    board = models.ForeignKey(Board, on_delete=models.CASCADE)  # 해당 댓글이 속한 게시판
    author = models.ForeignKey(AccountProfile, on_delete=models.CASCADE)  # 작성자
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성 시간
    is_deleted = models.BooleanField(default=False) # 삭제 여부
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        db_table = 'comment'
        app_label = 'comment'

    def getId(self):
        return self.id

    def getBoardId(self):
        return self.board.id

    def getAuthorNickname(self):
        return self.author.account_nickname if self.author else "알 수 없음"

    def getContent(self):
        return self.content

    def getCreatedAt(self):
        """댓글 작성 시간을 한국 시간으로 변환 (naive 처리 보정)"""
        dt = self.created_at
        if not is_aware(dt):
            dt = make_aware(dt)
        return localtime(dt).strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f"{self.getAuthorNickname()} - {self.content[:20]}..."
