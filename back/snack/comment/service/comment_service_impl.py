from django.core.exceptions import ObjectDoesNotExist
from comment.repository.comment_repository_impl import CommentRepositoryImpl
from comment.service.comment_service import CommentService
from comment.entity.comment import Comment
from board.entity.board import Board
from account_profile.entity.account_profile import AccountProfile
from account.entity.role_type import RoleType

class CommentServiceImpl(CommentService):
    __instance = None

    def __new__(cls):
        """ Singleton 패턴 적용 (한 번만 인스턴스 생성) """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__commentRepository = CommentRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        """ Singleton 인스턴스를 반환 """
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createComment(self, board: Board, author: AccountProfile, content: str) -> Comment:
        """ 새로운 댓글을 생성한다. """
        comment = Comment(board=board, author=author, content=content)
        return self.__commentRepository.save(comment)

    def findCommentById(self, comment_id: int) -> Comment:
        """ 댓글 ID로 특정 댓글을 찾는다. """
        return self.__commentRepository.findById(comment_id)

    def findAllCommentsByBoard(self, board: Board) -> list[Comment]:
        """ 특정 게시판의 모든 댓글을 조회한다. """
        return self.__commentRepository.findByBoard(board)

    def findAllCommentsByAuthor(self, author: AccountProfile) -> list[Comment]:
        """ 특정 작성자의 모든 댓글을 조회한다. """
        return self.__commentRepository.findByAuthor(author)

    def deleteComment(self, comment_id: int, user: AccountProfile) -> bool:
        """ 댓글 삭제 - 작성자 본인 또는 관리자만 가능 """
        comment = self.__commentRepository.findById(comment_id)
        if not comment:
            return False  # 댓글이 존재하지 않음

        # 관리자이면 삭제 가능
        if user.get_role() == RoleType.ADMIN:
            return self.__commentRepository.delete(comment_id)

        # 작성자 본인이면 삭제 가능
        if comment.author == user:
            return self.__commentRepository.delete(comment_id)

        return False  # 권한 없음