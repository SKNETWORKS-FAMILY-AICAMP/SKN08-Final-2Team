from abc import ABC, abstractmethod
from comment.entity.comment import Comment
from board.entity.board import Board
from account_profile.entity.account_profile import AccountProfile

class CommentService(ABC):

    @abstractmethod
    def createComment(self, board: Board, author: AccountProfile, content: str) -> Comment:
        """새로운 댓글을 생성한다."""
        pass

    @abstractmethod
    def findCommentById(self, comment_id: int) -> Comment:
        """댓글 ID로 특정 댓글을 찾는다."""
        pass

    @abstractmethod
    def findAllCommentsByBoard(self, board: Board) -> list[Comment]:
        """특정 게시판의 모든 댓글을 조회한다."""
        pass

    @abstractmethod
    def findAllCommentsByAuthor(self, author: AccountProfile) -> list[Comment]:
        """특정 작성자의 모든 댓글을 조회한다."""
        pass

    @abstractmethod
    def deleteComment(self, comment_id: int) -> bool:
        """댓글을 삭제한다."""
        pass
