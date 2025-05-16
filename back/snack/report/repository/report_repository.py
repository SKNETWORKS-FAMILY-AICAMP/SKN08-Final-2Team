from abc import ABC, abstractmethod
from report.entity.report import Report
from account.entity.account import Account
from typing import List

class ReportRepository(ABC):

    @abstractmethod
    def saveReport(self, reporter: Account, target_id: int, target_type: str, reason_type: str):
        pass

    @abstractmethod
    def findReportById(self, report_id: int) -> Report:
        pass

    @abstractmethod
    def findAllReports(self) -> List[Report]:
        pass

    @abstractmethod
    def updateReportStatus(self, report_id: int, admin: Account) -> Report:
        pass

    @abstractmethod
    def deleteReportById(self, report_id: int) -> None:
        pass