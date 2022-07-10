import logging

from aiogram import Dispatcher
from aiogram.types import Message, BotCommand

from tgbot.models.sql import User
from tgbot.services.lena import Lena, get_lena

logger = logging.getLogger(__name__)


def get_admin_commands():
    return [
        BotCommand('get_users', 'Получить зарегистрированных работников'),
        BotCommand('get_report', 'Получить отчет по проектам'),
        BotCommand('promote', 'Повысить пользователя до статуса админа'),
        BotCommand('hello', 'Поприветствовать бота')
    ]


async def answer_not_implemented(msg: Message):
    await msg.answer('Данная команда еще не реализована')


async def admin_command_hello(msg: Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}!')


async def admin_command_get_users(msg: Message):
    def format_user(user: User):
        return f'''<b>{user.fullname}</b>
            - id: {user.id}
            - youtrackId: {user.youtrackId}
            - telegramId: {user.telegramId}
            - timettaId: {user.timettaId}
            - is admin: {user.isAdmin}
        '''
    lena: Lena = get_lena()
    users = await lena.get_all_users_async()
    formatted = '\n'.join(list(map(format_user, users)))
    answer = 'Зарегистрированные пользователи:\n{}'.format(formatted)
    await msg.answer(text=answer)
    # await answer_not_implemented(msg)


async def admin_command_promote(msg: Message):
    await answer_not_implemented(msg)


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_command_hello, commands=['hello'])
    dp.register_message_handler(admin_command_get_users, commands=['get_users'])
    dp.register_message_handler(admin_command_promote, commands=['promote'])

