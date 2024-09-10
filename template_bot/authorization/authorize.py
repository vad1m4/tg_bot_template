from template_bot.logger.logger import log_cmd
from template_bot.global_vars import generic_markup as gm
from template_bot.authorization.vars import SUCCESS_TEXT, FAILURE_TEXT, AUTHORIZED_TEXT
from telebot import types, TeleBot  # type: ignore
import logging

logger = logging.getLogger("general")
user_logger = logging.getLogger("user_actions")


def authorize(message: types.Message, bot: TeleBot) -> None:
    log_cmd(message, "authorize")
    user_id = message.from_user.id
    generic_markup = gm(bot, message.from_user.id)
    if not bot.user_manager.is_authorized(user_id):
        phone_num = message.contact.phone_number

        if bot.user_manager.authorize(user_id, phone_num):
            log_text = f"Successfully authorised user {message.from_user.first_name} {message.from_user.last_name} via phone number ({phone_num})"
            logger.info(log_text)
            user_logger.info(log_text)
            bot.send_message(
                message.chat.id,
                SUCCESS_TEXT.format(phone_num=phone_num),
                parse_mode="html",
                reply_markup=generic_markup,
            )
        else:
            log_text = f"Failed to authorise user {message.from_user.first_name} {message.from_user.last_name} via phone number ({phone_num}): phone number blacklisted"
            logger.info(log_text)
            user_logger.info(log_text)
            reason = bot.user_manager.why_blacklist(phone_num)
            bot.send_message(
                message.chat.id,
                FAILURE_TEXT.format(phone_num=phone_num, reason=reason),
                parse_mode="html",
            )
    else:
        bot.send_message(
            message.chat.id,
            AUTHORIZED_TEXT,
            parse_mode="html",
            reply_markup=generic_markup,
        )
