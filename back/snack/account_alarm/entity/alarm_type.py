from django.db import models

class AlarmType(models.TextChoices):
    BOARD = 'BOARD', '게시글 알림'   # 게시글 관련 알림 (댓글, 좋아요 등)
    COMMENT = 'COMMENT', '댓글 알림' # 댓글 및 대댓글 관련 알림
    #NOTIFICATION = 'NOTIFICATION', '공지 사항'
