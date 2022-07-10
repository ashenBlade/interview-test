from datetime import datetime
import logging
from typing import Iterable

from aiogram import Dispatcher
from aiogram.types import BotCommand, Message

from tgbot.misc.command_pair import CommandPair

_logger = logging.getLogger(__name__)


async def user_command_start(msg: Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}!')


async def user_command_get_time(msg: Message):
    await msg.answer(f'Текущее время: {datetime.now().strftime("%-H:%-M:%-S")}')


_user_commands: Iterable[CommandPair] = [
    CommandPair(user_command_start, BotCommand('start', 'Начать диалог')),
    CommandPair(user_command_get_time, BotCommand('get_time', 'Получить текущее время'))
]


def register_user_handlers(dp: Dispatcher):
    for p in _user_commands:
        dp.register_message_handler(p.handler, commands=[p.command.command])
    # dp.register_message_handler(user_command_start, commands=['start'])
    # dp.register_message_handler(user_command_get_time, commands=['get_time'])


def get_user_commands() -> list[BotCommand]:
    return [p.command for p in _user_commands]
