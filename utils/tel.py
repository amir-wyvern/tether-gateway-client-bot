from telegram import InlineKeyboardButton, Bot
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

import logging

from dotenv import load_dotenv
import os
from pathlib import Path


dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


TOKEN_BOT = os.getenv('TOKEN_BOT')

bot = Bot(TOKEN_BOT)





async def delete_message(tel_id, message_id):
    try:
        await bot.delete_message(chat_id=tel_id, message_id=message_id)

    except TelegramError as error:
        logging.error(f"Error occurred while deleting message: {error}")


def create_key_button(ls_keys):
    ls = []
    for row in ls_keys:
        tmp = []
        for col in row:
            tmp.append(InlineKeyboardButton(col))

        ls.append(tmp)

    return ls
