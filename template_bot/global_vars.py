from telebot import types, TeleBot  # type: ignore

# --- Generic ---

generic_str = "Загальний"

none: types.ReplyKeyboardRemove = types.ReplyKeyboardRemove()

feedback_str = "Залишити відгук"
admin_str = "Меню адміна"


def generic_markup(bot: TeleBot, user_id: int) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    feedback = types.KeyboardButton(str(feedback_str))
    if bot.is_admin(user_id):
        admin = types.KeyboardButton(str(admin_str))
        return markup.add(admin, feedback)
    return markup.add(feedback)


# --- Cancel ---

cancel_str: str = "Назад"

cancel: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
    resize_keyboard=True, row_width=1
)
cancel_b = types.KeyboardButton(cancel_str)
cancel.add(cancel_b)


# --- Generic choice ---

yes_str: str = "Так"
no_str: str = "Ні"

generic_choice: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
    resize_keyboard=True, row_width=2
)
yes = types.KeyboardButton(yes_str)
no = types.KeyboardButton(no_str)
generic_choice.add(yes, no, cancel_b)


# ---  ---
