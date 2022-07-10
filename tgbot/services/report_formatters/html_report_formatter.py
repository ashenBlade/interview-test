from tgbot.models.report import Report
from tgbot.services.abstractions import IReportFormatter


class HtmlReportFormatter(IReportFormatter):
    def format(self, report: Report) -> str:
        raise NotImplemented()
