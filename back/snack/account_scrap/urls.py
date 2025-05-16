from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account_scrap.controller.account_scrap_controller import AccountScrapController

router = DefaultRouter()
router.register(r"account-scrap", AccountScrapController, basename='account-scrap')

urlpatterns = [
    path("", include(router.urls)),
    path('create', AccountScrapController.as_view({'post': 'createScrap'}), name='create-scrap'),
    path('delete/<int:scrap_id>', AccountScrapController.as_view({'delete': 'deleteScrap'}), name='delete-scrap'),
    path('my', AccountScrapController.as_view({'get': 'getMyScraps'}), name='get-my-scraps'),
]