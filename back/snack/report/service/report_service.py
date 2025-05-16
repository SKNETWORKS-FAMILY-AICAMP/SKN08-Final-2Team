from abc import ABC, abstractmethod
from report.entity.report import Report
from account.entity.account import Account
from typing import List

class ReportService(ABC):

    @abstractmethod
    def requestReport(self, reporter: Account, target_id: int, target_type: str, reason_type: str):
        pass

    @abstractmethod
    def getReportById(self, report_id: int) -> Report:
        pass

    @abstractmethod
    def getAllReports(self) -> List[Report]:
        pass

    @abstractmethod
    def updateReportStatus(self, report_id: int, admin: Account) -> Report:
        pass

    @abstractmethod
    def deleteReportById(self, report_id: int) -> None:
        self.__reportRepository.deleteReportById(report_id)