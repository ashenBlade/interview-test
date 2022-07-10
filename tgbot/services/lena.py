from typing import Iterable
from tgbot.models.sql import User
from tgbot.services.abstractions import ILena


class Lena(ILena):
    def __init__(self):
        pass

    async def get_all_users_async(self) -> Iterable[User]:
        return [User('Ivan Ivanov', 0, '', 0, False, 0)]
