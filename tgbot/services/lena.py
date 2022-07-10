from typing import Iterable
from tgbot.models.sql import User


class Lena:

    def __init__(self):
        pass

    async def get_all_users_async(self) -> Iterable[User]:
        return [User('Ivan Ivanov', 0, '', 0, False, 0)]


_lena: Lena | None = None


def get_lena():
    if not _lena:
        raise RuntimeError('Lena is not initialized')
    return _lena


def register_lena(lena: Lena):
    global _lena
    _lena = lena
