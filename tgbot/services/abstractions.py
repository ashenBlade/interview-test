import abc
from typing import Iterable
from tgbot.models.report import Report
from tgbot.models.sql import User


class ILena:
    @abc.abstractmethod
    async def get_all_users_async(self) -> Iterable[User]:
        pass


class IReportDownloader:
    @abc.abstractmethod
    async def download_report_async(self) -> Report:
        pass


class IReportFormatter:
    @abc.abstractmethod
    def format(self, report: Report) -> str:
        pass


class ITimesheetDownloader:
    @abc.abstractmethod
    async def download_timesheet_async(self, user_id):
        pass
