from template_bot.logger.logger import log_cmd
from telebot import types, TeleBot  # type: ignore
from template_bot.admin_commands.menu import menu
from template_bot.decorators.admin_only import admin_only


@admin_only
def user_stats(message: types.Message, bot: TeleBot):
    data = bot.user_storage.read()
    users = len(data["users"]) - 1
    bot.send_message(
        message.from_user.id,
        f"Усього користувачів: {users}",
    )
    menu(message, bot)
