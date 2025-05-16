from abc import ABC, abstractmethod
from board.entity.board import Board
from account_profile.entity.account_profile import AccountProfile

class BoardRepository(ABC):

    @abstractmethod
    def save(self, board: Board):
        """새로운 게시글을 저장한다."""
        pass

    @abstractmethod
    def findById(self, board_id: int):
        """ID로 게시글을 찾는다."""
        pass

    @abstractmethod
    def searchBoards(self, keywords):
        """검색어로 게시글 찾기기"""
        pass

    @abstractmethod
    def findAll(self):
        """모든 게시글을 조회한다."""
        pass

    @abstractmethod
    def findByAuthor(self, author: AccountProfile):
        """작성자의 게시글을 조회한다."""
        pass

    @abstractmethod
    def findByEndTimeRange(self, start_hour: int, end_hour: int):
        """특정 시간 범위에 모집 종료되는 게시글을 조회한다."""
        pass

    @abstractmethod
    def delete(self, board_id: int):
        """게시글을 삭제한다."""
        pass

    @abstractmethod
    def countBoardsByRestaurant(self):
        """식당별 게시글 수 반환"""
        pass
