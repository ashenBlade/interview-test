import logging
from typing import Iterable
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from aiogram.types import Message, BotCommand, ReplyKeyboardMarkup, KeyboardButton, ChatType, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery, Update
from aiogram.utils.callback_data import CallbackData
from setuptools.msvc import msvc9_find_vcvarsall

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


_get_report_callback_data = CallbackData('report', 'period')
_REPORT_YESTERDAY = 'yesterday'
_REPORT_CURR_WEEK = 'curr_week'
_REPORT_CURR_MONTH = 'curr_month'


async def admin_command_get_report(msg: Message):
    await msg.answer('Отчет за какой период вы хотите получить?', reply_markup=get_get_report_inline_keyboard())


def log_report_for_period(call: CallbackQuery, period: str):
    def format_period(p):
        return 'вчера' if p == _REPORT_YESTERDAY \
            else 'текущий месяц' if p == _REPORT_CURR_MONTH \
            else 'текущая неделя' if p == _REPORT_CURR_WEEK \
            else f'неизвестный период ({p})'
    _logger.info(f'Получен запрос на отчет за {format_period(period)} '
                 f'от админа {call.from_user.id} {call.from_user.full_name}')


async def admin_get_report_callback_yesterday(call: CallbackQuery):
    log_report_for_period(call, _REPORT_YESTERDAY)
    await call.message.answer(text='Пока нельзя получить отчет за вчера')


async def admin_get_report_callback_curr_week(call: CallbackQuery):
    log_report_for_period(call, _REPORT_CURR_WEEK)
    await call.message.answer(text='Пока нельзя получить отчет за текущую неделю')


async def admin_get_report_callback_curr_month(call: CallbackQuery):
    log_report_for_period(call, _REPORT_CURR_MONTH)
    await call.message.answer(text='Пока нельзя получить отчет за текущий месяц')


async def admin_get_report_callback_unknown(call: CallbackQuery):
    [_, period] = call.data.split(':')
    _logger.warning(f'Запрос на получение отчета за неизвествный период ({period}) '
                    f'от пользователя ({call.from_user.id} {call.from_user.full_name}). '
                    f'Callback data: {call.data}')
    await call.answer('Неизвестный период', show_alert=False)


_admin_commands: list[CommandPair] = [
    CommandPair(admin_command_get_report, BotCommand('get_report', 'Получить отчет за указанный период'), 'Отчет'),
    CommandPair(admin_command_get_users, BotCommand('get_users', 'Получить список зарегистированных пользователей'), 'Пользователи'),
    CommandPair(admin_command_promote, BotCommand('promote', 'Повысить пользователя до статуса админа'), 'Права админа'),
    CommandPair(admin_command_hello, BotCommand('admin', 'Начать сессию админа'), 'Я админ')
]


def get_get_report_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Вчера',
                                  callback_data=_get_report_callback_data.new(_REPORT_YESTERDAY))],
            [InlineKeyboardButton(text='Текущая неделя',
                                  callback_data=_get_report_callback_data.new(_REPORT_CURR_WEEK))],
            [InlineKeyboardButton(text='Текущий месяц',
                                  callback_data=_get_report_callback_data.new(_REPORT_CURR_MONTH))],
        ],
    )


def get_default_admin_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=pair.text)] for pair in _admin_commands
        ]
    )


def get_admin_commands():
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

    dp.register_callback_query_handler(admin_get_report_callback_yesterday,
                                       AdminFilter(is_admin=True),
                                       ChatTypeFilter([ChatType.PRIVATE]),
                                       _get_report_callback_data.filter(period=_REPORT_YESTERDAY))
    dp.register_callback_query_handler(admin_get_report_callback_curr_month,
                                       AdminFilter(is_admin=True),
                                       ChatTypeFilter([ChatType.PRIVATE]),
                                       _get_report_callback_data.filter(period=_REPORT_CURR_MONTH))
    dp.register_callback_query_handler(admin_get_report_callback_curr_week,
                                       AdminFilter(is_admin=True),
                                       ChatTypeFilter([ChatType.PRIVATE]),
                                       _get_report_callback_data.filter(period=_REPORT_CURR_WEEK))
    dp.register_callback_query_handler(admin_get_report_callback_unknown,
                                       AdminFilter(),
                                       ChatTypeFilter([ChatType.PRIVATE]),
                                       _get_report_callback_data.filter())

