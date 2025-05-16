from account_alarm.repository.account_alarm_repository_impl import AccountAlarmRepositoryImpl
from account_profile.entity.account_profile import AccountProfile
from board.entity.board import Board
from comment.entity.comment import Comment
from account.entity.account import Account


class AccountAlarmServiceImpl:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__accountAlarmRepository = AccountAlarmRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def getUserAlarmList(self, account_id):
        return self.__accountAlarmRepository.findUnreadAlarmsById(account_id)

    def readAlarm(self, alarm_id):
        return self.__accountAlarmRepository.saveReadAlarmById(alarm_id)

    def createBoardAlarm(self, board: Board, comment: Comment):
        return self.__accountAlarmRepository.saveBoardAlarm(board, comment)


    def createCommentAlarm(self, alarm_id):
        pass

    #
    # def createCommentAlarm(self, board: Board, comment: Comment, parent: Comment = None):
    #
    #     # 게시물 작성자 알림 (BOARD 타입)
    #     if board.author.account.id != comment.author.account.id:
    #         self.__createAlarm(
    #             recipient=board.author.account,
    #             board=board,
    #             comment=comment,
    #             alarm_type="BOARD"
    #         )
    #
    #     # 대댓글 알림 (COMMENT 타입)
    #     if parent:
    #         # 부모 댓글 작성자가 대댓글 작성자가 아닐 경우 (자기 대댓글 제외)
    #         if parent.author.account.id != comment.author.account.id:
    #             self.__createAlarm(
    #                 recipient=parent.author.account,
    #                 board=board,
    #                 comment=comment,
    #                 alarm_type="COMMENT"
    #             )
    #
    #
    # def __createAlarm(self, recipient: Account, board: Board, comment: Commnt, alarm_type: str):
    #     """
    #     일반적인 알림 생성 (다양한 상황에 사용 가능)
    #     """
    #     AccountAlarm.objects.create(
    #         recipient=recipient,
    #         board=board,
    #         comment=comment,
    #         alarm_type=alarm_type,
    #         is_unread=True
    #     )