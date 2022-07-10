import logging
from typing import Iterable
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from aiogram.types import Message, BotCommand, ReplyKeyboardMarkup, KeyboardButton, ChatType

from tgbot.filters.admin import AdminFilter
from tgbot.misc.command_pair import CommandPair
from tgbot.models.sql import User
from tgbot.services import get_lena

_logger = logging.getLogger(__name__)


async def answer_not_implemented(msg: Message):
    await msg.answer('Данная команда еще не реализована')


async def admin_command_hello(msg: Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}!', reply_markup=get_default_admin_keyboard())


async def admin_command_get_users(msg: Message):
    def format_user(user: User):
        return f'''<b>{user.fullname}</b>
            - id: {user.id}
            - youtrackId: {user.youtrackId}
            - telegramId: {user.telegramId}
            - timettaId: {user.timettaId}
            - is admin: {user.isAdmin}
        '''
    lena = get_lena()
    users = await lena.get_all_users_async()
    formatted = '\n'.join(list(map(format_user, users)))
    answer = 'Зарегистрированные пользователи:\n{}'.format(formatted)
    await msg.answer(text=answer)


async def admin_command_promote(msg: Message):
    await answer_not_implemented(msg)


async def admin_command_get_report(msg: Message):
    await answer_not_implemented(msg)


_admin_commands: list[CommandPair] = [
    CommandPair(admin_command_get_report, BotCommand('get_report', 'Получить отчет за указанный период'), 'Отчет'),
    CommandPair(admin_command_get_users, BotCommand('get_users', 'Получить список зарегистированных пользователей'), 'Пользователи'),
    CommandPair(admin_command_promote, BotCommand('promote', 'Повысить пользователя до статуса админа'), 'Права админа'),
    CommandPair(admin_command_hello, BotCommand('admin', 'Начать сессию админа'), 'Я админ')
]


def get_default_admin_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=pair.text)] for pair in _admin_commands
        ]
    )


def get_admin_commands() -> Iterable[BotCommand]:
    return [pair.command for pair in _admin_commands]


def register_admin_handlers(dp: Dispatcher):
    for p in _admin_commands:
        dp.register_message_handler(p.handler,
                                    AdminFilter(is_admin=True),
                                    ChatTypeFilter([ChatType.PRIVATE]),
                                    commands=[p.command.command])
        dp.register_message_handler(p.handler,
                                    AdminFilter(is_admin=True),
                                    ChatTypeFilter([ChatType.PRIVATE]),
                                    Text(equals=p.text))
