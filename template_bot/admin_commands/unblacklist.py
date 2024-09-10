from template_bot.logger.logger import log_cmd
from telebot import types, TeleBot  # type: ignore
from template_bot.admin_commands.vars import admin_markup  # type: ignore
from template_bot.global_vars import cancel
from template_bot.decorators.admin_only import admin_only
import logging

logger = logging.getLogger("general")
user_logger = logging.getLogger("user_actions")


@admin_only
def _unblacklist(message: types.Message, bot: TeleBot) -> None:
    log_cmd(message, "unblacklist 1")
    bot.send_message(
        message.from_user.id,
        f"🤖 Введіть номер або User ID користувача, якого ви хочете розблокувати.",
        parse_mode="html",
        reply_markup=cancel,
    )
    bot.register_next_step_handler(message, unblacklist, bot)


def unblacklist(message: types.Message, bot: TeleBot) -> None:
    log_cmd(message, "unblacklist 2")
    number = message.text
    if bot.user_manager.unblacklist(number):
        bot.send_message(
            message.from_user.id,
            f"✅ Успішно розблоковано {number}",
            parse_mode="html",
            reply_markup=admin_markup,
        )
        user_logger.info(
            f"Admin {message.from_user.first_name} {message.from_user.last_name} [{message.from_user.id}] unblocked {number}"
        )
        logger.info(
            f"Admin {message.from_user.first_name} {message.from_user.last_name} [{message.from_user.id}] unblocked {number}"
        )
    else:
        bot.send_message(
            message.from_user.id,
            f"❌ {number} не є заблокованим.",
            parse_mode="html",
            reply_markup=admin_markup,
        )
