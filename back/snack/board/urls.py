from django.urls import path
from rest_framework.routers import DefaultRouter
from board.controller.board_controller import BoardController

# DRF Router 설정
router = DefaultRouter()
router.register(r'board', BoardController, basename='board')

urlpatterns = [
    path('create', BoardController.as_view({'post': 'createBoard'}), name='create-board'),
    path('<int:board_id>', BoardController.as_view({'get': 'getBoard'}), name='get-board'),
    path('all', BoardController.as_view({'get': 'getAllBoards'}), name='get-all-boards'),
    path('search', BoardController.as_view({'get': 'searchBoards'}), name='search-boards'),
    path('author/<int:author_id>', BoardController.as_view({'get': 'getBoardsByAuthor'}), name='get-boards-by-author'),
    path('end-time-range/<int:start_hour>/<int:end_hour>', BoardController.as_view({'get': 'getBoardsByEndTimeRange'}), name='get-boards-by-end-time'),
    path('update/<int:board_id>', BoardController.as_view({'put': 'updateBoard', 'patch': 'partial_update'}), name='update-board'),
    path('delete/<int:board_id>', BoardController.as_view({'delete': 'deleteBoard'}), name='delete-board'),
    path('count', BoardController.as_view({'get': 'countBoardsPerRestaurant'}), name='count-boards-by-restaurant'),
]

# DRF router의 URL을 포함
urlpatterns += router.urls
