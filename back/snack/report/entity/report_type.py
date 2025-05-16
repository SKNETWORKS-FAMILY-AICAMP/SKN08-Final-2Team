from django.db import models


class ReportTargetType(models.TextChoices):
    BOARD = 'BOARD', '게시글'
    COMMENT = 'COMMENT', '댓글'


class ReportReasonType(models.TextChoices):
    SPAM = "SPAM", "불법광고"
    ABUSE = "ABUSE", "욕설/인신공격"
    REPEAT = "REPEAT", "도배성글/댓글반복"
    PRIVACY = "PRIVACY", "개인정보노출/사생활침해"
    SEXUAL = "SEXUAL", "음란성/선정성"
    FALSE_INFO = "FALSE_INFO", "허위정보/가짜리뷰"
    DISCRIMINATION = "DISCRIMINATION", "차별/혐오표현"
    ETC = "ETC", "기타부적절한행위"