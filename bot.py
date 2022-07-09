import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin_handlers
from tgbot.handlers.errors import register_error_handlers
from tgbot.handlers.user import register_user_handlers
from tgbot.middlewares.db import DbMiddleware
from tgbot.services.commands import register_default_commands_async


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin_handlers(dp)
    register_user_handlers(dp)
    register_error_handlers(dp)


async def register_default_commands(dp):
    await register_default_commands_async(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    # Exactly in this order
    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await register_default_commands(dp)
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
