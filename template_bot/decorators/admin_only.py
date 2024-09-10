from telebot import TeleBot, types  # type: ignore
from typing import Any, Callable
from template_bot.admin_commands.not_admin import not_admin


def admin_only(func: Callable) -> Callable:
    def wrapper(message: types.Message, bot: TeleBot):
        # for when the menu is called from an inline button where u can't pass the message but rather the "from_user" part of it is passed
        if isinstance(message, types.Message):
            from_user = message.from_user
        else:
            from_user = message

        if bot.is_admin(from_user.id):
            func(message, bot)
        else:
            not_admin(message, bot)

    return wrapper
