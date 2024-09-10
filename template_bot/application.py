from telebot import TeleBot  # type: ignore

from template_bot.storage.user_storage import JSONFileUserStorage
from template_bot.exception_handler.exception_handler import TGEBExceptionHandler
from template_bot.user_manager import UserManager

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

        self.user_manager = UserManager(self.user_storage)

        self.chunks: dict = {}
        logger.info("All services have been initalized successfully")
