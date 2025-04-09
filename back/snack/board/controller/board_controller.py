from django.http import JsonResponse
from rest_framework import status, viewsets
from board.service.board_service_impl import BoardServiceImpl
from account_profile.entity.account_profile import AccountProfile
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from restaurants.entity.restaurants import Restaurant
from account.service.account_service_impl import AccountServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl

class BoardController(viewsets.ViewSet):
    __boardService = BoardServiceImpl.getInstance()
    __accountService = AccountServiceImpl.getInstance()
    __redisService = RedisCacheServiceImpl.getInstance()

    def createBoard(self, request):
        postRequest = request.data
        userToken = request.headers.get("Authorization", "").replace("Bearer ", "")

        from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl
        redisService = RedisCacheServiceImpl.getInstance()
        account_id = redisService.getValueByKey(userToken)

        if not account_id:
            return JsonResponse({"error": "로그인 인증이 필요합니다.", "success": False}, status=status.HTTP_401_UNAUTHORIZED)

        title = postRequest.get("title")
        content = postRequest.get("content")
        image = request.FILES.get("image")
        end_time = postRequest.get("end_time")
        restaurant_id = postRequest.get("restaurant_id")

        if not title or not content or not end_time:
            return JsonResponse({"error": "필수 항목 누락", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            author = AccountProfile.objects.get(account__id=account_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "작성자 계정을 찾을 수 없습니다", "success": False}, status=status.HTTP_404_NOT_FOUND)

        restaurant = None
        if restaurant_id:
            restaurant = Restaurant(id=restaurant_id)

        board = self.__boardService.createBoard(title, content, author, image, end_time, restaurant)

        return JsonResponse({
            "success": True,
            "board_id": board.id,
            "title": board.title,
            "author_nickname": board.getAuthorNickname(),
            "image_url": board.getImageUrl(),
            "restaurant": board.restaurant.name if board.restaurant else None
        }, status=status.HTTP_201_CREATED)

    def getBoard(self, request, board_id):
        """특정 게시글 조회"""
        board = self.__boardService.findBoardById(board_id)
        if not board:
            return JsonResponse({"error": "게시글을 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({
            "board_id": board.id,
            "title": board.title,
            "content": board.content,
            "author_nickname": board.getAuthorNickname(),
            "created_at": board.getCreatedAt(),
            "end_time": board.getEndTime(),
            "status": board.status,
            "success": True
        }, status=status.HTTP_200_OK)
    
    def searchBoards(self, request):
        """검색어를 기반으로 게시글 검색 API (게시글 제목 + 지역 포함)"""
        keyword = request.GET.get("keyword")

        if not keyword:
            return JsonResponse({"error": "검색어(keyword) 파라미터가 필요합니다.", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        boards = self.__boardService.searchBoards(keyword)

        if not boards:
            return JsonResponse({"message": "검색된 게시글이 없습니다.", "success": True}, status=status.HTTP_200_OK)

        return JsonResponse({
            "success": True,
            "boards": [
                {"id": board.id, "title": board.title, "author": board.author.account_nickname, 
                 "restaurant": board.restaurant.name if board.restaurant else None}
                for board in boards
            ]
        }, status=status.HTTP_200_OK)

    def getAllBoards(self, request):
        """페이지네이션을 적용한 게시글 목록 조회"""
        page = int(request.GET.get("page", 1))  # 기본값: 1페이지
        per_page = int(request.GET.get("per_page", 10))  # 기본값: 10개씩

        boards = self.__boardService.findAllBoards().order_by('-created_at')  # 최신순 정렬

        # 페이지네이션 적용
        paginator = Paginator(boards, per_page)
        page_obj = paginator.get_page(page)

        board_list = [
            {
                "board_id": board.id,
                "title": board.title,
                "author_nickname": board.getAuthorNickname(),
                "created_at": board.getCreatedAt(),
                "end_time": board.getEndTime(),
                "status": board.status,
                "image_url": board.getImageUrl(),
            }
            for board in page_obj.object_list
        ]
        return JsonResponse({
            "success": True,
            "boards": board_list,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number
        }, status=status.HTTP_200_OK)

    def getBoardsByAuthor(self, request, author_id):
        """특정 작성자의 게시글 조회"""
        try:
            author = AccountProfile.objects.get(account__id=author_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "작성자를 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)

        boards = self.__boardService.findBoardsByAuthor(author)
        board_list = [
            {
                "board_id": board.id,
                "title": board.title,
                "created_at": board.getCreatedAt(),
                "end_time": board.getEndTime(),
                "status": board.status
            }
            for board in boards
        ]

        return JsonResponse({"success": True, "boards": board_list}, status=status.HTTP_200_OK)

    def getBoardsByEndTimeRange(self, request, start_hour, end_hour):
        """특정 시간대 (예: 07:00~10:00) 내 모집 종료되는 게시글 조회"""
        boards = self.__boardService.findBoardsByEndTimeRange(start_hour, end_hour)
        board_list = [
            {
                "board_id": board.id,
                "title": board.title,
                "created_at": board.getCreatedAt(),
                "end_time": board.getEndTime(),
                "status": board.status
            }
            for board in boards
        ]

        return JsonResponse({"success": True, "boards": board_list}, status=status.HTTP_200_OK)

    def updateBoard(self, request, board_id):
        """게시글 수정"""
        postRequest = request.data
        user_id = postRequest.get("user_id")
        title = postRequest.get("title")
        content = postRequest.get("content")
        image = request.FILES.get("image")
        end_time = postRequest.get("end_time")
        restaurant = postRequest.get("restaurant")

        if not user_id:
            return JsonResponse({"error": "user_id가 필요합니다.", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = AccountProfile.objects.get(account__id=user_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "사용자를 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)

        updated_board = self.__boardService.updateBoard(board_id, user, title, content, image, end_time)

        if not updated_board:
            return JsonResponse({"error": "게시글을 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({
            "success": True,
            "message": "게시글이 수정되었습니다.",
            "board_id": updated_board.id,
            "title": updated_board.title,
            "updated_at": updated_board.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "restaurant" : updated_board.restaurant
        }, status=status.HTTP_200_OK)

    def deleteBoard(self, request, board_id):
        """게시글 삭제"""
        user_id = request.query_params.get("user_id")

        if not user_id:
            return JsonResponse({"error": "user_id가 필요합니다.", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = AccountProfile.objects.get(account__id=user_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "사용자를 찾을 수 없습니다.", "success": False}, status=status.HTTP_404_NOT_FOUND)

        deleted = self.__boardService.deleteBoard(board_id, user)
        if not deleted:
            return JsonResponse({"error": "삭제 권한이 없습니다.", "success": False}, status=status.HTTP_403_FORBIDDEN)

        return JsonResponse({"success": True, "message": "게시글이 삭제되었습니다."}, status=status.HTTP_200_OK)