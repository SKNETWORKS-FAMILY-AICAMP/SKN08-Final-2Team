from django.urls import path
from rest_framework.routers import DefaultRouter
from comment.controller.comment_controller import CommentController

# DRF Router 설정
router = DefaultRouter()
router.register(r'comment', CommentController, basename='comment')

urlpatterns = [
    path('create', CommentController.as_view({'post': 'createComment'}), name='create-comment'),
    path('<int:comment_id>', CommentController.as_view({'get': 'getComment'}), name='get-comment'),
    path('board/<int:board_id>', CommentController.as_view({'get': 'getAllCommentsByBoard'}), name='get-comments-by-board'),
    path('author/<int:author_id>', CommentController.as_view({'get': 'getAllCommentsByAuthor'}), name='get-comments-by-author'),
    path('delete/<int:comment_id>', CommentController.as_view({'delete': 'deleteComment'}), name='delete-comment'),
    path('reply', CommentController.as_view({'post': 'createReply'})),
    path('update/<int:comment_id>', CommentController.as_view({'put': 'updateComment'}), name='update-comment'),

]

# DRF router의 URL을 포함
urlpatterns += router.urls
