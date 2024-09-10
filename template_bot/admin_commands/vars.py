from telebot import types  # type: ignore
from template_bot.global_vars import cancel_b

blacklist_str: str = "Заблокувати номер"
unblacklist_str: str = "Розблокувати номер"
announcement_str: str = "Оголошення"
logs_str: str = "Передивитися логи"
user_stats_str: str = "Кільікість користувачів"

admin_markup: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
    resize_keyboard=True, row_width=2
)
blacklist = types.KeyboardButton(blacklist_str)
unblacklist = types.KeyboardButton(unblacklist_str)
announcement = types.KeyboardButton(announcement_str)
logs = types.KeyboardButton(logs_str)
user_stats = types.KeyboardButton(user_stats_str)
admin_markup.add(
    blacklist,
    unblacklist,
    announcement,
    logs,
    user_stats,
    cancel_b,
)
