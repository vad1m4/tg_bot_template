from telebot import types  # type: ignore

login_str: str = "Авторизуватися"

login_markup: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
    resize_keyboard=True, row_width=1
)
login = types.KeyboardButton(text=login_str, request_contact=True)
login_markup.add(login)


start_text = "👋 Привіт<b> {name}</b>! \n\n(emj) Я - ваш персональний помічник, який буде (bot's purpose).\n\nДля початку роботи зі мною, авторизуйтеся за допомогою номеру телефона."
disclaimer_text = "⚠️ (disclaimer) \nБот знаходиться у стані активної розробки. Недоліки, недостовірність інформації, відгуки та побажання можна залишити командою /feedback"
