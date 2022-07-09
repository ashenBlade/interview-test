import logging

from aiogram import Dispatcher
from aiogram.types import Message, BotCommand

logger = logging.getLogger(__name__)


async def admin_command_start(message: Message):
    await message.answer("Hello, admin!")


def get_admin_commands():
    return [
        BotCommand('get_users', 'Получить список пользователей из базы данных'),
        BotCommand('report', 'Получить отчет по проектам')
    ]

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_command_start, commands=['start'])