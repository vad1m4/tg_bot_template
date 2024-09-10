from template_bot.logger.logger import log_cmd
from telebot import types, TeleBot  # type: ignore
from template_bot.admin_commands.vars import admin_markup  # type: ignore
from template_bot.decorators.admin_only import admin_only


@admin_only
def menu(data: types.Message, bot: TeleBot) -> None:
    if isinstance(data, types.Message):
        from_user = data.from_user
    else:
        from_user = data
    log_cmd(from_user, "admin menu")
    bot.send_message(
        from_user.id,
        f"💻 Оберіть одну з опцій.",
        parse_mode="html",
        reply_markup=admin_markup,
    )
