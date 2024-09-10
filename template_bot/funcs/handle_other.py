from template_bot.logger.logger import log_cmd
from template_bot.global_vars import generic_markup as gm
from telebot import types, TeleBot  # type: ignore
from template_bot.decorators.authorized_only import authorized_only


@authorized_only
def handle_other(message: types.Message, bot: TeleBot) -> None:
    log_cmd(message, "handler_other")
    generic_markup = gm(bot, message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"🤖 Я ще не вмію сприймати такі повідомлення. Щоб мною користуватися, оберіть одну з опцій нижче.",
        parse_mode="html",
        reply_markup=generic_markup,
    )
