from datetime import datetime
import logging

from aiogram import Dispatcher
from aiogram.types import BotCommand, Message

logger = logging.getLogger(__name__)


def get_user_commands():
    return [
        BotCommand('start', 'Начать диалог'),
        BotCommand('get_time', 'Получить текущее время'),
    ]


async def user_command_start(msg: Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}!')


async def user_command_get_time(msg: Message):
    await msg.answer(f'Текущее время: {datetime.now().strftime("%-H:%-M:%-S")}')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(user_command_start, commands=['start'])
    dp.register_message_handler(user_command_get_time, commands=['get_time'])
