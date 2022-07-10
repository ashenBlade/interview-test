from tgbot.models.timesheet import Timesheet
from tgbot.services.abstractions import ILena, IReportFormatter, IReportDownloader, ITimesheetDownloader

_lena: ILena | None = None


def get_lena() -> ILena:
    if not _lena:
        raise RuntimeError('Lena is not initialized')
    return _lena


def register_lena(lena: ILena) -> None:
    global _lena
    _lena = lena


_report_downloader: IReportDownloader | None = None


def get_report_downloader() -> IReportDownloader:
    if not _report_downloader:
        raise RuntimeError('Report downloader in not initialized')
    return _report_downloader


def register_report_downloader(report_downloader: IReportDownloader):
    global _report_downloader
    _report_downloader = report_downloader


_report_formatter: IReportFormatter | None = None


def get_report_formatter() -> IReportFormatter:
    if not _report_formatter:
        raise RuntimeError('Report formatter is not initialized')


def register_report_formatter(formatter: IReportFormatter):
    global _report_formatter
    _report_formatter = formatter


_timesheet_downloader: ITimesheetDownloader | None = None


def get_timesheet_downloader() -> Timesheet:
    if not _timesheet_downloader:
        raise RuntimeError('Timesheet downloader in not initialized')
    return _timesheet_downloader


def register_timesheet_downloader(timesheet: ITimesheetDownloader):
    global _timesheet_downloader
    _timesheet_downloader = timesheet