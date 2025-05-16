from report.entity.report import Report
from account.entity.account import Account
from report.repository.report_repository import ReportRepository
from typing import List


class ReportRepositoryImpl(ReportRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return  cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def saveReport(self, reporter: Account, target_id: int, target_type: str, reason_type: str) ->Report:
        report = Report.objects.create(
            reporter=reporter,
            target_id=target_id,
            target_type=target_type,
            reason_type=reason_type
        )
        return report

    def findReportById(self, report_id: int) -> Report:
        return Report.objects.get(id=report_id)

    def findAllReports(self) -> List[Report]:
        return list(Report.objects.all())

    def updateReportStatus(self, report_id: int, admin: Account) -> Report:
        report = Report.objects.get(id=report_id)
        report.mark_processed(admin)
        return report

    def deleteReportById(self, report_id: int) -> None:
        try:
            report = Report.objects.get(id=report_id)
            report.delete()
        except Report.DoesNotExist:
            raise  # 상위에서 처리