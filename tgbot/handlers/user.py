from datetime import datetime
import logging
from typing import Iterable

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from aiogram.types import BotCommand, Message, ReplyKeyboardMarkup, KeyboardButton, ChatType

from tgbot.misc.command_pair import CommandPair

_logger = logging.getLogger(__name__)


async def user_command_start(msg: Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}!', reply_markup=get_default_user_keyboard())


async def user_command_get_time(msg: Message):
    await msg.answer(f'Текущее время: {datetime.now().strftime("%-H:%-M:%-S")}')


_user_commands: Iterable[CommandPair] = [
    CommandPair(user_command_start, BotCommand('user', 'Начать диалог'), 'Я работник'),
    CommandPair(user_command_get_time, BotCommand('get_time', 'Получить текущее время'), 'Время')
]


def get_default_user_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(p.text)] for p in _user_commands
        ],
        resize_keyboard=True)


def register_user_handlers(dp: Dispatcher):
    for p in _user_commands:
        dp.register_message_handler(p.handler,
                                    ChatTypeFilter([ChatType.PRIVATE]),
                                    commands=[p.command.command])
        dp.register_message_handler(p.handler,
                                    ChatTypeFilter([ChatType.PRIVATE]),
                                    Text(equals=p.text))


def get_user_commands() -> list[BotCommand]:
    return [p.command for p in _user_commands]
