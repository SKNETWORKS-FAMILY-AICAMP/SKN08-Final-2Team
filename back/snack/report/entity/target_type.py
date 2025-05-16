from django.db import models


class ReportTargetType(models.TextChoices):
    BOARD = 'BOARD', '게시글'
    COMMENT = 'COMMENT', '댓글'

