from abc import ABC, abstractmethod
from comment.entity.comment import Comment
from board.entity.board import Board
from account_profile.entity.account_profile import AccountProfile

class CommentRepository(ABC):

    @abstractmethod
    def save(self, comment: Comment):
        """새로운 댓글을 저장한다."""
        pass

    @abstractmethod
    def findById(self, comment_id: int):
        """ID로 댓글을 찾는다."""
        pass

    @abstractmethod
    def findByBoard(self, board: Board):
        """특정 게시판의 모든 댓글을 조회한다."""
        pass

    @abstractmethod
    def findByAuthor(self, author: AccountProfile):
        """특정 작성자의 모든 댓글을 조회한다."""
        pass

    @abstractmethod
    def delete(self, comment_id: int):
        """댓글을 삭제한다."""
        pass
