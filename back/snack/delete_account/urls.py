from django.urls import path
from delete_account.controller.delete_account_controller import DeleteAccountController

urlpatterns = [
    path("account/deactivate", DeleteAccountController.as_view({"post": "deactivateAccount"}), name="deactivate-account"),
]
