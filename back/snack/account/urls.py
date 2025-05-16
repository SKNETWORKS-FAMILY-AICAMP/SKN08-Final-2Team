from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.controller.account_controller import AccountController

router = DefaultRouter()
router.register(r"account", AccountController, basename='account')

urlpatterns = [
    path("", include(router.urls)),
    path("create", AccountController.as_view({"post": "createAccount"}), name="create-account"),
    path("get", AccountController.as_view({"get": "getAccount"}), name="get-account"),
    path("update-last-used/<str:email>", AccountController.as_view({"put": "updateLastUsed"}), name="update-last-used"),
    path("email", AccountController.as_view({"post": "requestEmail"}), name="request-email"),
    path("suspend", AccountController.as_view({"post": "suspendAccount"}), name="suspend-account"),
    path("suspended-list", AccountController.as_view({"get": "getSuspendedAccounts"}), name="get-suspended-accounts"),
    path("unsuspend/<int:account_id>", AccountController.as_view({"put": "unsuspendAccount"}), name="unsuspend-account"),
    path("ban", AccountController.as_view({"post": "banAccount"}), name="ban-account"),
    path("banned-list", AccountController.as_view({"get": "getBannedAccounts"}), name="get-banned-accounts"),
    path("unban/<int:account_id>", AccountController.as_view({"put": "unbanAccount"}), name="unban-account"),
]