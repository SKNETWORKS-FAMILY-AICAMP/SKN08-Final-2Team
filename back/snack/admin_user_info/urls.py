from django.urls import path, include
from admin_user_info.controller.admin_user_info_controller import AdminUserInfoController

urlpatterns = [
    path('<int:account_id>', AdminUserInfoController.as_view({'get': 'getUserInfo'}), name='request-user-info'),
    path('list', AdminUserInfoController.as_view({'get': 'getUserInfoList'}), name='user-info-list'),
]
