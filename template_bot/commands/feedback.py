from template_bot.logger.logger import log_cmd
from template_bot.global_vars import cancel, cancel_str
from template_bot.funcs.generic import generic
from template_bot.config import admins
from telebot import types, TeleBot  # type: ignore
from template_bot.decorators.authorized_only import authorized_only


@authorized_only
def _feedback(message: types.Message, bot: TeleBot) -> None:
    bot.send_message(
        message.chat.id,
        f"📲 Чудово! Напищіть ваш відгук у наступному повідомленні.",
        parse_mode="html",
        reply_markup=cancel,
    )
    bot.register_next_step_handler(message, feedback, bot)


def feedback(message: types.Message, bot: TeleBot) -> None:
    if message.text == cancel_str:
        generic(message, bot)
    else:
        bot.send_message(
            message.from_user.id,
            f"✅ Відгук успішно залишено!",
            parse_mode="html",
        )
        generic(message, bot)
        for admin in admins:
            bot.send_message(
                admin,
                f'❕ {message.from_user.first_name} {message.from_user.last_name} [{message.from_user.id}] залишили відгук!\n\n"{message.text}"',
                parse_mode="html",
            )
