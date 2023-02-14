from utils.user import user_redis

from telegram import Update
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardMarkup

from cache.cache_session import (
    set_position,
    set_cache
)
from utils.tel import create_key_button


@user_redis
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    # resp = user_exist_check(update.effective_chat.id, get_redis_cache().__next__())
    set_position(update.effective_chat.id, 'menu', db)
    set_cache(update.effective_chat.id, {}, db)

    if user['login'] == 'logined':
        ls = create_key_button(strings["login_menu_buttons"])
        options =ReplyKeyboardMarkup(ls , resize_keyboard=True)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['login_menu'], reply_markup=options)
    
    else:
        ls = create_key_button(strings["no_login_menu_buttons"])
        options =ReplyKeyboardMarkup(ls , resize_keyboard=True)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['no_login_menu'],reply_markup=options)

