import asyncio
import logging

import environs
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats

from tgbot.config import load_config, Config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers import \
    register_error_handlers, \
    register_admin_handlers, \
    register_group_handlers, \
    register_user_handlers
from tgbot.handlers.admin import get_admin_commands
from tgbot.handlers.group import get_group_commands
from tgbot.handlers.user import get_user_commands
from tgbot.middlewares.db import DbMiddleware
from tgbot.services.locator import register_lena, register_report_downloader, register_report_formatter
from tgbot.services.lena import Lena
from tgbot.services.report_downloader import YouTrackReportDownloader
from tgbot.services.report_formatter import HtmlReportFormatter


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin_handlers(dp)
    register_user_handlers(dp)
    register_group_handlers(dp)
    register_error_handlers(dp)


async def register_default_commands_async(dp: Dispatcher):
    await dp.bot.set_my_commands(get_admin_commands(), BotCommandScopeAllPrivateChats())
    await dp.bot.set_my_commands(get_user_commands(), BotCommandScopeAllPrivateChats())
    await dp.bot.set_my_commands(get_group_commands(), BotCommandScopeAllGroupChats())


def register_dependencies(config: Config):
    register_lena(Lena())
    youtrack_server = config.yt.address
    timetta_server = config.tt.address
    register_report_downloader(YouTrackReportDownloader())
    register_report_formatter(HtmlReportFormatter())


async def main():
    config = load_config(".env")

    logging.basicConfig(
        level=logging.DEBUG,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
    logger = logging.getLogger(__name__)

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_dependencies(config)

    # Exactly in this order
    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await register_default_commands_async(dp)
    except Exception as ex:
        logger.error('Could not register default commands', exc_info=ex)
        return
    finally:
        await bot.close()
        await dp.storage.close()
        await dp.storage.wait_closed()

    try:
        await dp.start_polling()
    except Exception as ex:
        logger.error('Unhandled exception occurred in polling mode', exc_info=ex)
    finally:
        await bot.close()
        await dp.storage.close()
        await dp.storage.wait_closed()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
