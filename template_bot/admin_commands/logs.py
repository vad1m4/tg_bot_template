from template_bot.logger.logger import log_cmd
from telebot import types, TeleBot  # type: ignore
from template_bot.global_vars import cancel, cancel_str
from template_bot.admin_commands.menu import menu  # type: ignore
from template_bot.decorators.admin_only import admin_only
import logging
import os
from pathlib import Path


logger = logging.getLogger("general")
user_logger = logging.getLogger("user_actions")


@admin_only
def logs_menu(message: types.Message, bot: TeleBot):
    log_cmd(message, "logs_menu")
    # filenames = [:10]
    # search_dir = "/mydir/"
    os.chdir("general_logs/")
    filenames = os.listdir()
    # files = [os.path.join(search_dir, f) for f in files] # add path to each file
    filenames.sort(key=lambda x: os.path.getmtime(x))
    filenames.reverse()
    filenames = filenames[:30]
    if len(filenames) > 0:
        formatted_filenames = []
        for i, filename in enumerate(filenames, start=1):
            stripped_filename = filename.removeprefix("bot_").removesuffix(".txt")
            new_filename = f"{stripped_filename}_new.txt"
            formatted_filenames.append(f"{i}. {new_filename}")
        message_text = (
            "\n".join(formatted_filenames)
            + "\n\n📄 Введіть номер файлу який вас цікавить."
        )
        bot.send_message(message.from_user.id, message_text, reply_markup=cancel)
        bot.register_next_step_handler(message, send_logs, bot, filenames)
    else:
        bot.send_message(message.from_user.id, "❌ Немає жодного файлу з логами.")
        menu(message, bot)
    os.chdir("..")


def send_file(message: types.Message, bot: TeleBot, filename: str):
    file = open(filename, "rb")
    bot.send_document(message.chat.id, file)


def send_logs(message: types.Message, bot: TeleBot, filenames: list):
    if message.text == cancel_str:
        menu(message, bot)
    else:
        try:
            if int(message.text) <= len(filenames) and int(message.text) > 0:
                filename = Path.cwd() / f"general_logs/{filenames[int(message.text)-1]}"
                with open(filename, "r") as file:
                    lines = file.readlines()
                    chunks = [lines[i : i + 50] for i in range(0, len(lines), 50)]
                edit_message = bot.send_message(message.from_user.id, ".")
                bot.chunks[edit_message.id] = [
                    chunks,
                    filename,
                ]
                update_page(message, edit_message.id, message.from_user.id, bot, 0)

            else:
                raise ValueError
        except ValueError:
            bot.send_message(
                message.from_user.id,
                f"🤖 Не розумію. Оберіть відповідь від 1 до {len(filenames)}.",
                parse_mode="html",
                reply_markup=cancel_str,
            )
            bot.register_next_step_handler(message, send_logs, bot, filenames)


def update_page(
    message: types.Message,
    message_id: int,
    chat_id: int,
    bot: TeleBot,
    page_number: int,
):
    # chat_id = message.from_user.id
    # message_id = message.id
    chunks = bot.chunks[message_id][0]
    if 0 <= page_number < len(chunks):
        text = "".join(chunks[page_number])
        markup = types.InlineKeyboardMarkup()

        if page_number > 0:
            markup.add(
                types.InlineKeyboardButton(
                    "⬆️ Попередня", callback_data=f"page_{page_number - 1}"
                )
            )

        if page_number < len(chunks) - 1:
            markup.add(
                types.InlineKeyboardButton(
                    "⬇️ Наступна", callback_data=f"page_{page_number + 1}"
                )
            )

        markup.add(types.InlineKeyboardButton("❌ Вийти", callback_data="exit"))
        markup.add(
            types.InlineKeyboardButton("📄 Переглянути файл", callback_data="send_file")
        )

        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup
        )
    else:
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text="Сторінки скінчилися."
        )


def handle_page_navigation(call, bot: TeleBot):
    if call.data in ["exit", "send_file"]:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Ви вийшли з режиму перегляду файлу.",
        )
        if call.data == "send_file":
            send_file(call.message, bot, bot.chunks[call.message.id][1])
        bot.chunks.pop(call.message.id)
        menu(call.from_user, bot)
    else:
        page_number = int(call.data.split("_")[1])
        update_page(
            call.message,
            call.message.message_id,
            call.message.chat.id,
            bot,
            page_number,
        )
