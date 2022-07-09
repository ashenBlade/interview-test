from aiogram import Dispatcher
from aiogram.types import BotCommand, Message


def get_group_commands():
    return [
        BotCommand('init', 'Инициализировать рабочий чат')
    ]


async def group_command_init(msg: Message):
    await msg.answer('Команда еще не реализована')


def register_group_handlers(dp: Dispatcher):
    dp.register_message_handler(group_command_init, commands=['init'])
