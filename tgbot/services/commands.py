from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats

def get_group_commands():
    return [
        BotCommand('init', 'Инициализировать рабочий чат')
    ]


def get_admin_commands():
    return [
        BotCommand('get_users', 'Получить список пользователей из базы данных'),
        BotCommand('report', 'Получить отчет по проектам')
    ]


def get_user_commands():
    return [
        BotCommand('start', 'Начать диалог'),
        BotCommand('get_time', 'Получить текущее время'),
    ]


async def register_default_commands_async(dp: Dispatcher):
    bot = dp.bot
    await bot.set_my_commands(get_user_commands(), BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(get_group_commands(), BotCommandScopeAllGroupChats())

    # Change to BotCommandScopeChat(chat_id) in production
    await bot.set_my_commands(get_admin_commands(), BotCommandScopeAllPrivateChats())
