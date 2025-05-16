from django.core.exceptions import ObjectDoesNotExist
from board.repository.board_repository_impl import BoardRepositoryImpl
from board.service.board_service import BoardService
from board.entity.board import Board
from account_profile.entity.account_profile import AccountProfile
from account.entity.role_type import RoleType  # 역할 체크 추가
from utility.auth_utils import is_authorized_user
from utility.s3_client import S3Client

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

    def createBoard(self, title: str, content: str, author: AccountProfile,
                    end_time=None, restaurant=None, image_url: str = None) -> Board:
        print("✅ createBoard 호출됨")
        board = Board(
            title=title,
            content=content,
            author=author,
            end_time=end_time,
            restaurant=restaurant,
            image_url=image_url
        )

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
#여기
    def updateBoard(self, board_id: int, user: AccountProfile, title: str = None, content: str = None,
                    end_time=None, restaurant=None, image=None, image_url: str = None) -> Board:
        # ✅ board 변수 미리 조회
        board = self.__boardRepository.findById(board_id)
        if not board:
            raise ObjectDoesNotExist("게시글을 찾을 수 없습니다")

        if user.get_role() == "ADMIN" or board.author == user:
            # ✅ 기존 이미지 삭제 처리 (다르면만)
            if image_url and board.image_url and board.image_url != image_url:
                try:
                    s3 = S3Client.getInstance()
                    key = board.image_url.split(f"https://{s3.bucket_name}.s3.amazonaws.com/")[-1]
                    s3.delete_file(key)
                    print("✅ 기존 이미지 삭제됨:", key)
                except Exception as e:
                    print("⚠️ 기존 이미지 삭제 실패:", e)

            # ✅ 명시적으로 덮어쓰기
            board.title = title if title is not None else board.title
            board.content = content if content is not None else board.content
            board.end_time = end_time if end_time is not None else board.end_time
            board.restaurant = restaurant
            board.image_url = image_url if image_url is not None else board.image_url

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

        # ✅ 이미지도 함께 삭제
        if board.image_url:
            try:
                s3 = S3Client.getInstance()
                key = board.image_url.split(f"https://{s3.bucket_name}.s3.amazonaws.com/")[-1]
                s3.delete_file(key)
                print("✅ 삭제된 이미지 제거 완료:", key)
            except Exception as e:
                print("⚠️ 이미지 삭제 실패:", e)

        self.__boardRepository.delete(board_id)
        return True, 200, "게시글이 삭제되었습니다."
    
    def countBoardsByRestaurant(self):
        return self.__boardRepository.countBoardsByRestaurant()
