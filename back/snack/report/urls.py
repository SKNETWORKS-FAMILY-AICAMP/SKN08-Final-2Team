from django.urls import path, include
from rest_framework.routers import DefaultRouter
from report.controller.report_controller import ReportController

# DRF Router 설정
router = DefaultRouter()
router.register(r'', ReportController, basename='report')

urlpatterns = [
    path('request', ReportController.as_view({'post': 'requestReport'}), name='request-report'),
    path('detail/<int:request_id>', ReportController.as_view({'get': 'getReportDetail'}), name='report-detail'),
    path('list', ReportController.as_view({'get': 'getReportsList'}), name='report-list'),
    path('delete/<int:request_id>', ReportController.as_view({'delete': 'deleteReport'}), name='report-delete'),
    path('update/<int:request_id>', ReportController.as_view({'put': 'updateReportStatus'}), name='report-update'),

    path('', include(router.urls)),
]