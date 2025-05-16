from django.db import models
from django.utils import timezone
from account.entity.account import Account
from report.entity.report_type import ReportReasonType
from report.entity.target_type import ReportTargetType

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey(Account, on_delete=models.CASCADE)  # 신고자
    target_id = models.IntegerField()  # 신고 대상
    target_type = models.CharField(max_length=20, choices=ReportTargetType.choices)  # 신고된 곳(게시글, 댓글)
    reason_type = models.CharField(max_length=50, choices=ReportReasonType.choices)  # 신고 사유
    created_at = models.DateTimeField(auto_now_add=True)  # 신고 시점
    processed = models.BooleanField(default=False)  # 처리 여부
    processed_at = models.DateTimeField(null=True, blank=True)  # 처리된 시점
    processed_by = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name="reports_processed")  # 처리 관리자

    class Meta:
        db_table = 'report'
        app_label = 'report'

    def mark_processed(self, admin: Account):
        self.processed = True
        self.processed_at = timezone.now()
        self.processed_by = admin
        self.save()
