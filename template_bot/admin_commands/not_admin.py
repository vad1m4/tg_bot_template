from template_bot.logger.logger import log_cmd
from telebot import types, TeleBot  # type: ignore


def not_admin(message: types.Message, bot: TeleBot) -> None:
    log_cmd(message, "not_admin")
    bot.send_message(
        message.from_user.id,
        f" \n\n❌ Ви не є адміном цього бота.",
        parse_mode="html",
    )
