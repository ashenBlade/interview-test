import logging

from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.utils.exceptions import MessageError, TelegramAPIError

logger = logging.getLogger(__name__)


async def global_error_handler(update: Update, ex: Exception):
    if not isinstance(ex, TelegramAPIError):
        logger.error(f'Not Telegram API exception caught: {ex}')
        return True

    if isinstance(ex, MessageError):
        logger.error('Message error')
        return True

    if isinstance(ex, TelegramAPIError):
        logger.error(f'Telegram api error {ex}')
        return True

    return False


def register_error_handlers(dp: Dispatcher):
    dp.register_errors_handler(global_error_handler)