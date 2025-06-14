from board.entity.board import Board
from comment.entity.comment import Comment
from account_alarm.entity.account_alarm import AccountAlarm
from account_profile.entity.account_profile import AccountProfile
# from django.utils import timezone
# from datetime import timedelta

class AccountAlarmRepositoryImpl:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def findUnreadAlarmsById(self, account_id):
        alarms = (
            AccountAlarm.objects
            .filter(recipient=account_id, is_unread=True)  # 미읽은 알림만 조회
            .select_related('comment__author__account', 'board')  # 댓글, 댓글 작성자, 게시글을 JOIN (성능 최적화)
            .order_by('-alarm_created_at')  # 최신 알림 우선 정렬
        )

        alarm_list = []
        for alarm in alarms:
            comment = alarm.comment
            author = comment.author if comment else None

            alarm_data = {
                "alarm_id": alarm.id,
                "board_id": alarm.board.id,
                "board_title": alarm.board.title,
                "comment_id": comment.id if comment else None,
                "comment_created_at": comment.created_at if comment else None,
                "comment_author_id": alarm.comment.author.account.id if alarm.comment and alarm.comment.author else None,
                "comment_author_nickname": author.account_nickname if author else None,
                "comment_content": comment.content if comment else None
            }
            alarm_list.append(alarm_data)
            
        return alarm_list

    def saveReadAlarmById(self, alarm_id):
        try:
            alarm = AccountAlarm.objects.get(id=alarm_id)
            alarm.is_unread = False
            alarm.save()
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("알림을 찾을 수 없습니다.")


    def saveBoardAlarm(self, board: Board, comment: Comment):
        AccountAlarm.objects.create(
            alarm_type="BOARD",
            is_unread=True,
            board=board,
            recipient=board.author.account,
            comment=comment
        )
