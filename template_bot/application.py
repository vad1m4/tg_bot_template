from telebot import TeleBot  # type: ignore

from template_bot.storage.storage import JSONFileUserStorage
from template_bot.exception_handler.exception_handler import TGEBExceptionHandler
from template_bot.time.time import get_date, get_unix
from template_bot.commands.start import start

# from electricity_bot.logger import add_logger
from template_bot.config import admins

from pathlib import Path

import logging


logger = logging.getLogger("general")


class Application(TeleBot):
    def __init__(self, token: str, debug: bool = False) -> None:

        self.debug = debug

        ### Telegram bot init

        exception_handler = TGEBExceptionHandler()

        super().__init__(token)
        logger.info("Telegram bot initialized")

        ### Storage init

        self.user_storage = JSONFileUserStorage(Path.cwd() / "users.json")
        logger.info("Storage initialized")

        self.chunks: dict = {}
        logger.info("All services have been initalized successfully")
        ### User commands

    ### Check if user_id is in self.admins

    def is_admin(self, user_id: int) -> bool:
        if not user_id in admins:
            return False
        else:
            return True
