import logging

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand, Message

from tgbot.misc.command_pair import CommandPair

_logger = logging.getLogger(__name__)


async def group_command_init(msg: Message):
    _logger.debug('Запрос на инициализацию рабочего чата ({}, {}) от пользователя {}'
                  .format(msg.chat.id,
                          msg.chat.full_name,
                          msg.from_user.id))
    await msg.answer('Команда еще не реализована')

_group_commands = [
    CommandPair(group_command_init, BotCommand('init', 'Инициализировать рабочий чат'), 'Начать')
]


def register_group_handlers(dp: Dispatcher):
    for p in _group_commands:
        dp.register_message_handler(p.handler, commands=[p.command.command])
        dp.register_message_handler(p.handler, Text(equals=p.text))


def get_group_commands():
    return [p.command for p in _group_commands]

