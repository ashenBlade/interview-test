from .html_report_formatter import HtmlReportFormatter
from ..abstractions.report_formatter import IReportFormatter


def get_formatter() -> IReportFormatter:
    return HtmlReportFormatter()

