from abc import ABC, abstractmethod
from board.entity.board import Board
from account_profile.entity.account_profile import AccountProfile

class BoardService(ABC):
    @abstractmethod
    def createBoard(self, title: str, content: str, author: AccountProfile, image=None, end_time=None, restaurant=None) -> Board:
        """새로운 게시글을 생성한다."""
        pass

    @abstractmethod
    def findBoardById(self, board_id: int) -> Board:
        """게시글 ID로 특정 게시글을 찾는다."""
        pass

    @abstractmethod
    def findAllBoards(self) -> list[Board]:
        """모든 게시글을 조회한다."""
        pass

    @abstractmethod
    def searchBoards(self, keyword: str):
        pass

    @abstractmethod
    def findBoardsByAuthor(self, author: AccountProfile) -> list[Board]:
        """특정 작성자의 게시글 목록을 조회한다."""
        pass

    @abstractmethod
    def findBoardsByEndTimeRange(self, start_hour: int, end_hour: int) -> list[Board]:
        """특정 시간 범위(예: 07:00~10:00) 사이에 모집 종료되는 게시글을 조회한다."""
        pass

    @abstractmethod
    def updateBoard(self, board_id: int, title: str = None, content: str = None, image=None, end_time=None) -> Board:
        """게시글을 수정한다."""
        pass

    @abstractmethod
    def deleteBoard(self, board_id: int) -> bool:
        """게시글을 삭제한다."""
        pass

    @abstractmethod
    def deleteBoardWithToken(self, board_id: int) -> bool:
        """게시글 삭제 유효성 검사."""
        pass

    @abstractmethod
    def countBoardsByRestaurant(self):
        """식당별 게시글 수 반환"""
        pass