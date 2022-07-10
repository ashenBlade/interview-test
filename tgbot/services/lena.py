import logging
from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker, Session

from tgbot.models.sql import User
from tgbot.services.abstractions import ILena


class Lena(ILena):
    def __init__(self, engine: AsyncEngine):
        self.__logger = logging.getLogger(__name__)
        self.__engine = engine

    async def get_all_users_async(self) -> Iterable[User]:
        async_session = sessionmaker(self.__engine, class_=AsyncSession)
        async with async_session() as session:
            session: AsyncSession
            stmt = select(User).order_by(User.id)
            result = await session.execute(stmt)

            l = list(result.scalars().all())
            self.__logger.info(f'users received {l}')
            return l

        #
        # return [User('Ivan Ivanov', 0, '', 0, False, 0)]
