from telegram import InlineKeyboardButton, Bot
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from dotenv import load_dotenv

from handlers.menu_handler import menu
from cache.cache_session import (
    set_lang
)

from utils.user import user_redis 
from utils.tel import delete_message 


@user_redis
async def select_lang(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):
    
    data = update.callback_query.data
    lang = data.split(':')[1]

    set_lang(update.effective_chat.id, lang, db)
    await delete_message(update.effective_chat.id, update.callback_query.message.id)

    await menu(update, context)