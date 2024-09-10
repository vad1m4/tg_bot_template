from template_bot.logger.logger import log_cmd
from template_bot.commands.vars import login_markup, start_text  # , disclaimer_text
from telebot import types, TeleBot  # type: ignore


def start(message: types.Message, bot: TeleBot) -> None:
    log_cmd(message, "start")
    bot.send_message(
        message.chat.id,
        start_text.format(name=message.from_user.first_name),
        parse_mode="html",
        reply_markup=login_markup,  # remove this line if you're using a disclaimer
    )
    # bot.send_message(
    #     message.from_user.id,
    #     disclaimer_text,
    #     parse_mode="html",
    #     reply_markup=login_markup,
    # )
