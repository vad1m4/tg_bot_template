from template_bot.logger.logger import log_cmd
from template_bot.authorization.vars import NOT_AUTHORIZED_TEXT
from template_bot.commands.vars import login_markup  # , disclaimer_text
from telebot import types, TeleBot  # type: ignore


def not_authorized(message: types.Message, bot: TeleBot) -> None:
    log_cmd(message, "not authorized")
    bot.send_message(
        message.chat.id,
        NOT_AUTHORIZED_TEXT,
        parse_mode="html",  # change these to vars
        reply_markup=login_markup,
    )
