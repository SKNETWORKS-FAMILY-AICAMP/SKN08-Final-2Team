from django.core.exceptions import ObjectDoesNotExist
from board.repository.board_repository_impl import BoardRepositoryImpl
from board.service.board_service import BoardService
from board.entity.board import Board
from account_profile.entity.account_profile import AccountProfile
from account.entity.role_type import RoleType  # 역할 체크 추가
from utility.auth_utils import is_authorized_user

class BoardServiceImpl(BoardService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__boardRepository = BoardRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createBoard(self, title: str, content: str, author: AccountProfile, image=None, end_time=None, restaurant=None) -> Board:
        print("✅ createBoard 호출됨")
        board = Board(title=title, content=content, author=author, end_time=end_time, restaurant=restaurant)

        if image:
            print("🟢 이미지 존재함. S3 업로드 시도")
            board.image_url = self.__boardRepository.uploadImageToS3(image)
            print("✅ S3 업로드 완료, image_url:", board.image_url)
        else:
            print("⚠️ 이미지 없음")

        return self.__boardRepository.save(board)

    def findBoardById(self, board_id: int) -> Board:
        return self.__boardRepository.findById(board_id)

    def searchBoards(self, keyword: str):
        return self.__boardRepository.searchBoards(keyword)

    def findAllBoards(self) -> list[Board]:
        return self.__boardRepository.findAll()

    def findBoardByTitle(self, title: str):
        return self.__boardRepository.findByTitle(title)

    def findBoardsByAuthor(self, author: AccountProfile) -> list[Board]:
        return self.__boardRepository.findByAuthor(author)

    def findBoardsByEndTimeRange(self, start_hour: int, end_hour: int) -> list[Board]:
        return self.__boardRepository.findByEndTimeRange(start_hour, end_hour)

    def updateBoard(self, board_id: int, user: AccountProfile, title: str = None, content: str = None, image=None, end_time=None, restaurant=None) -> Board:
        board = self.__boardRepository.findById(board_id)
        if not board:
            raise ObjectDoesNotExist("게시글을 찾을 수 없습니다")

        if user.get_role() == "ADMIN" or board.author == user:
            if title:
                board.title = title
            if content:
                board.content = content
            if end_time:
                board.end_time = end_time
            if image:
                board.image_url = self.__boardRepository.uploadImageToS3(image)
            if restaurant:
                board.restaurant = restaurant

            return self.__boardRepository.save(board)

        raise PermissionError("게시글을 수정할 권한이 없습니다.")

    def deleteBoard(self, board_id: int, user: AccountProfile) -> bool:
        board = self.__boardRepository.findById(board_id)
        if not board:
            return False

        if user.get_role() == "ADMIN":
            return self.__boardRepository.delete(board_id)

        if board.author.account.id == user.account.id:
            return self.__boardRepository.delete(board_id)

        return False

    def deleteBoardWithToken(self, board_id: int, userToken: str) -> tuple[bool, int, str]:
        board = self.__boardRepository.findById(board_id)
        if not board:
            return False, 404, "게시글을 찾을 수 없습니다."

        authorized, status_code, message = is_authorized_user(board, userToken)
        if not authorized:
            return False, status_code, message

        self.__boardRepository.delete(board_id)
        return True, 200, "게시글이 삭제되었습니다."
