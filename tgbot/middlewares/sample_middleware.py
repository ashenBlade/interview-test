import logging

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update



class SampleMiddleware(BaseMiddleware):
    def __int__(self):
        self.logger = logging.getLogger(__name__ + ' SampleMiddleware')
    async def on_pre_process_update(self, update: Update, data: dict):
        l = self.logger
        l.info('Pre process update')
        data['sample'] = 'This will come to on_post_process_update'

        if update.message:
            user = update.message.from_user
        elif update.callback_query:
            user = update.callback_query.from_user
        else:
            return

        banned = [1, 2, 3]
        if user.id in banned:
            raise Cancel




