from aiogram.types import BotCommand


def get_group_commands():
    return [
        BotCommand('init', 'Инициализировать рабочий чат')
    ]