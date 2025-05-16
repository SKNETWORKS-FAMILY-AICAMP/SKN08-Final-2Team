from django.apps import AppConfig
from django.db import models
from account_alarm.entity.alarm_type import AlarmType
from board.entity.board import Board
from comment.entity.comment import Comment
from account.entity.account import Account
from account_profile.entity.account_profile import AccountProfile



class AccountAlarm(models.Model):
    id = models.AutoField(primary_key=True)          # alarm_id
    alarm_type = models.CharField(
        max_length=15,
        choices=AlarmType.choices,  # AlarmType에서 정의된 타입 사용
        default=AlarmType.COMMENT
    )
    is_unread = models.BooleanField(default=True)  # 알림 읽음 여부
    alarm_created_at = models.DateTimeField(auto_now_add=True)  # 알림 생성 시간

    board = models.ForeignKey(Board, on_delete=models.CASCADE)  # board_id
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recipient')  # account_id, 알림 수신자
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)  # comment_id

    class Meta:
        db_table = 'account_alarm'
        app_label = 'account_alarm'
        ordering = ['-alarm_created_at'] # 생성된 시간 내림차순 정렬 (최근 알림이 위로)



    # board_title = models.CharField(max_length=255, null=True, blank=True)  # Board 제목
    # comment_author = models.CharField(max_length=100, null=True, blank=True)  # Comment 작성자 (nickname)
    # comment_content = models.TextField(null=True, blank=True)  # Comment 내용
    # comment_created_at = models.DateTimeField(null=True, blank=True)  # Comment 작성 시간


    # def save(self, *args, **kwargs):
    #     # Board 제목 자동 저장
    #     if self.board and not self.board_title:
    #         self.board_title = self.board.title
    #
    #     # Comment 정보 자동 저장
    #     if self.comment:
    #         if not self.comment_author:
    #             self.comment_author = self.comment.author.account_nickname if self.comment.author else "Unknown"
    #         if not self.comment_content:
    #             self.comment_content = self.comment.content
    #         if not self.comment_created_at:
    #             self.comment_created_at = self.comment.created_at
    #
    #     super().save(*args, **kwargs)