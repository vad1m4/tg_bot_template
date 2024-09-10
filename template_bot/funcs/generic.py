from template_bot.global_vars import generic_markup as gm

from telebot import types, TeleBot  # type: ignore
from template_bot.decorators.authorized_only import authorized_only


@authorized_only
def generic(message: types.Message, bot: TeleBot) -> None:
    generic_markup = gm(bot, message.from_user.id)
    name = message.from_user.first_name
    bot.send_message(
        message.chat.id,
        f"👋 Чим я можу тобі допомогти,<b> {name}</b>?",
        parse_mode="html",
        reply_markup=generic_markup,
    )
