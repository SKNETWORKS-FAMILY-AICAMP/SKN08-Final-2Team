from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account_alarm.controller.account_alarm_controller import AccountAlarmController

router = DefaultRouter()
router.register(r"alarm", AccountAlarmController, basename='alarm')

urlpatterns = [
    path("", include(router.urls)),
    path("get-alarms", AccountAlarmController.as_view({"get": "getUserAlarms"}), name="get-user-alarms"),
    path("read-alarm", AccountAlarmController.as_view({"patch": "readUserAlarm"}), name="read-user-alarm"),

]