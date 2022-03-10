#Copyright-2021 // Python Telegram Bot 13.6 Updated by @noobanon
#Copyright (C) 2021 Free Software @noobanon @FakeMasked , Inc.[ https://t.me/noobanon https://t.me/FakeMasked ]
#Everyone is permitted to copy and distribute verbatim copies
#of this license document, but changing it is not allowed.
#The GNGeneral Public License is a free, copyleft license for
#software and other kinds of works.
#PTB13 Updated by @noobanon


import telegram.ext as tg
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters
from AnieRobot.modules.sql.antispam_sql import is_user_gbanned
import AnieRobot.modules.sql.blacklistusers_sql as sql
try:
    from AnieRobot import CUSTOM_CMD
except:
    CUSTOM_CMD = False

CMD_STARTERS = CUSTOM_CMD or ('!', '/')


class CustomCommandHandler(tg.CommandHandler):
    def __init__(self, command, callback, **kwargs):
        if "admin_ok" in kwargs:
            del kwargs["admin_ok"]
        super().__init__(command, callback, **kwargs)

    def check_update(self, update):
        if not isinstance(update, Update) or not update.effective_message:
            return
        message = update.effective_message

        try: 
           user_id = update.effective_user.id
        except:
           user_id = None
        if user_id and is_user_gbanned(user_id):
            return
        if user_id and sql.is_user_blacklisted(update.effective_user.id):
            return False

        if message.text and len(message.text) > 1:
            fst_word = message.text.split(None, 1)[0]
            if len(fst_word) > 1 and any(fst_word.startswith(start) for start in ('/', '!')):
                args = message.text.split()[1:]
                command = fst_word[1:].split('@')
                command.append(message.bot.username)  # in case the command was sent without a username

                if (
                    command[0].lower() not in self.command
                    or command[1].lower() != message.bot.username.lower()
                ):
                    return None

                if filter_result := self.filters(update):
                    return args, filter_result
                else:
                    return False
