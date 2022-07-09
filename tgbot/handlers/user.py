import logging
from aiogram import Dispatcher
from aiogram.types import BotCommand

logger = logging.getLogger(__name__)


def get_user_commands():
    return [
        BotCommand('start', 'Начать диалог'),
        BotCommand('get_time', 'Получить текущее время'),
    ]


def register_user_handlers(dp: Dispatcher):
    pass
