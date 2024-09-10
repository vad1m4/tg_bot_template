from telebot import TeleBot, types  # type: ignore
from typing import Any, Callable
from template_bot.authorization.not_authorized import not_authorized


def authorized_only(func: Callable) -> Callable:
    def wrapper(message: types.Message | Any, bot: TeleBot):
        # for when the menu is called from an inline button where u can't pass the message but rather the "from_user" part of it is passed
        if isinstance(message, types.Message):
            from_user = message.from_user
        else:
            from_user = message

        if bot.user_storage.is_authorized(from_user.id):
            func(message, bot)
        else:
            not_authorized(message, bot)

    return wrapper
