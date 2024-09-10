from telebot import TeleBot  # type: ignore
from telebot import apihelper
import logging

logger = logging.getLogger("general")


def notify(bot: TeleBot, group: str | list, message: str):
    if isinstance(group, list):
        group_list = group
    else:
        group_list = bot.user_storage.read()[group]
    for user_id in group_list:
        try:
            bot.send_message(
                user_id,
                message,
                parse_mode="html",
            )
            logger.info(f"Notified: {user_id}")
            continue
        except apihelper.ApiTelegramException as e:
            if e.error_code == 403:
                logger.error(
                    f"{user_id} has blocked the bot. Removing them from the list"
                )
                bot.user_storage.delete(user_id, group)
            elif e.error_code in [401, 404]:
                logger.error(f"Could not access {user_id}. Removing them from the list")
                bot.user_storage.delete(user_id, group)
            continue
        except Exception as e:
            logger.error(
                f"{e} occured. Take actions regarding this error as soon as possible."
            )
            continue
    logger.info(f"Users notified.")
