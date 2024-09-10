from template_bot.logger.logger import log_cmd
from template_bot.commands.vars import login_markup  # , disclaimer_text
from telebot import types, TeleBot  # type: ignore


def not_authorized(message: types.Message, bot: TeleBot) -> None:
    log_cmd(message, "not authorized")
    bot.send_message(
        message.chat.id,
        f" \n\n❌ Ви не авторизовані. Для початку роботи зі мною, авторизуйтеся за допомогою номеру телефона.",
        parse_mode="html",  # change these to vars
        reply_markup=login_markup,
    )
