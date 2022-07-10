from tgbot.services.abstractions import ITimesheetDownloader


class TimesheetDownloader(ITimesheetDownloader):
    async def download_timesheet_async(self, user_id):
        raise NotImplemented()

