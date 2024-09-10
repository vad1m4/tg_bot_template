from template_bot.logger.logger import log_cmd
from telebot import types, TeleBot  # type: ignore
from template_bot.admin_commands.vars import admin_markup  # type: ignore
from template_bot.global_vars import cancel, cancel_str
from template_bot.admin_commands.menu import menu  # type: ignore
from template_bot.funcs.notify import notify
from template_bot.decorators.admin_only import admin_only
import logging


logger = logging.getLogger("general")
user_logger = logging.getLogger("user_actions")


@admin_only
def _announce(message: types.Message, bot: TeleBot):
    log_cmd(message, "announce 1")
    if message.text == cancel_str:
        menu(message, bot)
    else:
        bot.send_message(
            message.from_user.id,
            f"⌨️ Напишіть ваше оголошення.",
            parse_mode="html",
            reply_markup=cancel,
        )
        bot.register_next_step_handler(message, announce, bot)


def announce(message: types.Message, bot: TeleBot):
    log_cmd(message, "announce 2")
    if message.text == cancel_str:
        menu(message, bot)
    else:
        logger.info(
            f"Admin {message.from_user.first_name} {message.from_user.last_name} [{message.from_user.id}] announced to users, text: {message.text}"
        )
        user_logger.info(
            f"Admin {message.from_user.first_name} {message.from_user.last_name} [{message.from_user.id}] announced to users, text: {message.text}"
        )
        group_list = list(bot.user_storage.read()["users"].keys())[1:]
        notify(bot, group_list, f"⚠️ Оголошення від адміністратора:\n\n{message.text}")
        bot.send_message(
            message.from_user.id,
            f"✅ {len(group_list)} отримали ваше оголошення.",
            parse_mode="html",
            reply_markup=admin_markup,
        )

        menu(message, bot)
