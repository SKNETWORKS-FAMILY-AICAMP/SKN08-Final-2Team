from report.entity.report import Report
from account.entity.account import Account
from report.service.report_service import ReportService
from report.repository.report_repository_impl import ReportRepositoryImpl
from typing import List
from django.core.exceptions import ValidationError

class ReportServiceImpl(ReportService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__reportRepository = ReportRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def requestReport(self, reporter: Account, target_id: int, target_type: str, reason_type: str) -> Report:

        # 중복 신고 확인
        existing_report = Report.objects.filter(
            reporter=reporter,
            target_id=target_id,
            target_type=target_type
        ).first()

        if existing_report:
            raise ValidationError("이미 해당 항목을 신고하였습니다.")

        report = self.__reportRepository.saveReport(reporter, target_id, target_type, reason_type)
        return report

    def getReportById(self, report_id: int) -> Report:
        return self.__reportRepository.findReportById(report_id)

    def getAllReports(self) -> List[Report]:
        return self.__reportRepository.findAllReports()

    def updateReportStatus(self, report_id: int, admin: Account) -> Report:
        return self.__reportRepository.updateReportStatus(report_id, admin)

    def deleteReportById(self, report_id: int) -> None:
        self.__reportRepository.deleteReportById(report_id)
