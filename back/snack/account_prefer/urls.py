from django.urls import path
from account_prefer.controller.account_prefer_controller import SaveAccountPreference

urlpatterns = [
    path('save', SaveAccountPreference.as_view(), name='account_prefer_save'),
    path('<int:account_id>', SaveAccountPreference.as_view(), name='account_prefer_get')
]