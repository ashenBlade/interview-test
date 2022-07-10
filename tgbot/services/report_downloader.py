from tgbot.models.report import Report
from tgbot.services.abstractions import IReportDownloader


class YouTrackReportDownloader(IReportDownloader):
    async def download_report_async(self) -> Report:
        raise NotImplemented()
