from aiogram.types import BotCommand
from typing import Callable, Any, Coroutine


class CommandPair:
    def __init__(self, func, command: BotCommand):
        self.handler = func
        self.command = command
