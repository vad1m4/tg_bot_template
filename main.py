# credentials
from template_bot.config import TOKEN, TOKEN_DEBUG

# app
from template_bot.application import Application

# logging
from template_bot.logger.logger import setup_logging

# time
from template_bot.utils import get_date, get_time

### global_vars
import template_bot.global_vars as gv
import template_bot.admin_commands.vars as av

### commands
# start
from template_bot.commands.start import start

# generic
from template_bot.funcs.generic import generic

# authorize
from template_bot.authorization.authorize import authorize

# feedback
from template_bot.commands.feedback import _feedback

# handle_other
from template_bot.funcs.handle_other import handle_other


### admin
from template_bot.admin_commands.menu import menu
from template_bot.admin_commands.blacklist import _blacklist_
from template_bot.admin_commands.unblacklist import _unblacklist
from template_bot.admin_commands.announce import _announce
from template_bot.admin_commands.logs import (
    logs_menu,
    send_file,
    update_page,
    handle_page_navigation,
)
from template_bot.admin_commands.user_stats import user_stats


from telebot import TeleBot, types  # type: ignore
from logging import INFO, DEBUG
import argparse


def register_user_handlers(bot: TeleBot) -> None:
    # start
    bot.register_message_handler(start, commands=["start"], pass_bot=True)
    # authorize
    bot.register_message_handler(authorize, content_types=["contact"], pass_bot=True)
    # feedback
    bot.register_message_handler(_feedback, regexp=gv.feedback_str, pass_bot=True)
    bot.register_message_handler(_feedback, commands=["feedback"], pass_bot=True)
    # generic
    bot.register_message_handler(generic, regexp=gv.cancel_str, pass_bot=True)


def register_admin_handlers(bot: TeleBot) -> None:
    # menu
    bot.register_message_handler(menu, commands=["adminmenu"], pass_bot=True)
    bot.register_message_handler(menu, regexp=gv.admin_str, pass_bot=True)
    # block
    bot.register_message_handler(_blacklist_, commands=["block"], pass_bot=True)
    bot.register_message_handler(_blacklist_, regexp=av.blacklist_str, pass_bot=True)
    # unblock
    bot.register_message_handler(_unblacklist, commands=["unblock"], pass_bot=True)
    bot.register_message_handler(_unblacklist, regexp=av.unblacklist_str, pass_bot=True)
    # announce
    bot.register_message_handler(_announce, commands=["announce"], pass_bot=True)
    bot.register_message_handler(_announce, regexp=av.announcement_str, pass_bot=True)
    # logs menu
    bot.register_message_handler(logs_menu, commands=["logs"], pass_bot=True)
    bot.register_message_handler(logs_menu, regexp=av.logs_str, pass_bot=True)
    # user stats
    bot.register_message_handler(user_stats, commands=["user_stats"], pass_bot=True)
    bot.register_message_handler(user_stats, regexp=av.user_stats_str, pass_bot=True)
    # inline button query handler
    bot.register_callback_query_handler(
        handle_page_navigation,
        func=lambda call: call.data.startswith("page_")
        or call.data in ["exit", "send_file"],
        pass_bot=True,
    )


def register_other_handler(bot: TeleBot) -> None:
    # triggered if no other handlers worked (e.g. the user tried to use a non-existent command/gave bad input)
    bot.register_message_handler(handle_other, func=lambda message: True, pass_bot=True)


def main() -> None:
    parser = argparse.ArgumentParser("TTGB")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    file_name = f"bot_{get_date()}_{get_time('-')}.txt"

    setup_logging(file_name, DEBUG if args.debug else INFO)

    token = TOKEN_DEBUG if args.debug else TOKEN
    app = Application(token, args.debug)
    register_admin_handlers(app)
    register_user_handlers(app)
    register_other_handler(app)
    app.infinity_polling()


if __name__ == "__main__":
    main()
