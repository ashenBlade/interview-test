from aiogram import Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from tgbot.handlers.admin import get_admin_commands
from tgbot.handlers.group import get_group_commands
from tgbot.handlers.user import get_user_commands


async def register_default_commands_async(dp: Dispatcher):
    await dp.bot.set_my_commands(get_user_commands(), BotCommandScopeAllPrivateChats())
    await dp.bot.set_my_commands(get_group_commands(), BotCommandScopeAllGroupChats())
    await dp.bot.set_my_commands(get_admin_commands(), BotCommandScopeAllPrivateChats())
