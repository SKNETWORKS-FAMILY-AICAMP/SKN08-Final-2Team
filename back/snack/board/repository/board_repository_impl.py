from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from uuid import uuid4
from board.entity.board import Board
from board.repository.board_repository import BoardRepository
from account_profile.entity.account_profile import AccountProfile
from utility.s3_client import S3Client
from restaurants.entity.restaurants import Restaurant

class BoardRepositoryImpl(BoardRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__s3_client = S3Client.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance
        
    def uploadImageToS3(self, image_file):
        try:
            print("🚀 S3 업로드 시작: 파일명 =", image_file.name)
            s3Client = S3Client.getInstance()

            if not image_file:
                print("❌ 이미지 파일이 없음")
                return None

            file_name = f"board_images/{uuid4()}_{image_file.name}"
            file_url = s3Client.upload_file(image_file, file_name)
            print("✅ S3 업로드 성공, URL =", file_url)
            return file_url

        except Exception as e:
            print("❌ S3 업로드 실패:", e)
            raise Exception(f"S3 업로드 실패: {str(e)}")



    def save(self, board: Board):
        """새로운 게시글을 저장한다."""
        board.save()
        return board

    def findById(self, board_id: int):
        """ID로 게시글을 찾는다."""
        try:
            return Board.objects.get(id=board_id)
        except ObjectDoesNotExist:
            return None

    def findAll(self):
        """모든 게시글을 조회한다."""
        return Board.objects.all()
    
    def searchBoards(self, keyword: str):
        """검색어를 기반으로 게시글 검색 (게시글 제목 + 식당 주소 포함)"""

        title_matched_boards = Board.objects.filter(title__icontains=keyword)

        restaurants = Restaurant.objects.filter(address__icontains=keyword)

        location_matched_boards = Board.objects.filter(restaurant__in=restaurants)

        return title_matched_boards | location_matched_boards

    def findByAuthor(self, author: AccountProfile):
        """작성자의 게시글을 조회한다."""
        return list(Board.objects.filter(author=author))

    def findByEndTimeRange(self, start_hour: int, end_hour: int):
        """특정 시간 범위에 모집 종료되는 게시글을 조회한다."""
        return list(Board.objects.filter(
            end_time__hour__gte=start_hour,
            end_time__hour__lte=end_hour
        ))

    def delete(self, board_id: int):
        """게시글을 삭제한다."""
        board = self.findById(board_id)
        if board:
            board.delete()
            return True
        return False
