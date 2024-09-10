from template_bot.logger.logger import log_cmd
from telebot import types, TeleBot  # type: ignore
from template_bot.admin_commands.vars import admin_markup  # type: ignore
from template_bot.global_vars import cancel
from template_bot.decorators.admin_only import admin_only
import logging

logger = logging.getLogger("general")
user_logger = logging.getLogger("user_actions")


@admin_only
def _blacklist_(message: types.Message, bot: TeleBot) -> None:
    log_cmd(message, "blacklist 1")
    bot.send_message(
        message.from_user.id,
        f"🤖 Введіть номер або User ID користувача, якого ви хочете заблокувати.",
        parse_mode="html",
        reply_markup=cancel,
    )
    bot.register_next_step_handler(message, _blacklist, bot)


def _blacklist(message: types.Message, bot: TeleBot) -> None:
    log_cmd(message, "blacklist 2")
    try:
        if message.text[0] == "+":
            number = message.text
        else:
            number = int(message.text)
        bot.send_message(
            message.from_user.id,
            f"❌ Напишіть причину блокування:",
            parse_mode="html",
            reply_markup=cancel,
        )
        bot.register_next_step_handler(message, blacklist, bot, number)
    except:
        bot.send_message(
            message.from_user.id,
            f"❌ {number} не є коректним номером або Telegram ID",
            parse_mode="html",
            reply_markup=cancel,
        )
        bot.register_next_step_handler(message, _blacklist, bot)


def blacklist(message: types.Message, bot: TeleBot, number: int | str) -> None:
    log_cmd(message, "blacklist 3")
    bot.user_manager.blacklist(number, message.text)
    user_logger.info(
        f"Admin {message.from_user.first_name} {message.from_user.last_name} [{message.from_user.id}] blocked {number}, reason: {message.text}"
    )
    logger.info(
        f"Admin {message.from_user.first_name} {message.from_user.last_name} [{message.from_user.id}] blocked {number}, reason: {message.text}"
    )
    bot.send_message(
        message.from_user.id,
        f"✅ Успішно заблоковано {number}",
        parse_mode="html",
        reply_markup=admin_markup,
    )
