from utils.user import user_redis, create_key_button


from telegram import Update
from telegram.ext import ContextTypes

from cache.cache_session import (
    set_position
)

@user_redis
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    set_position(update.effective_chat.id, 'support', db)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['support_text'])

@user_redis
async def get_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    set_position(update.effective_chat.id, 'menu', db)
    # save the requests in db
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['support_ans'])

