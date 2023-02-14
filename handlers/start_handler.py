from utils.user import user_redis


from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from cache.cache_session import set_referal_link


@user_redis
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):
    # send request for get info user
        # resp = user_exist_check(update.effective_chat.id, get_redis_cache().__next__())
    if user['login'] == 'not login':
        referal_link = context.args[0] if len(context.args) > 0 else None
        if referal_link:
            set_referal_link(referal_link)
    
    options = InlineKeyboardMarkup([[
        InlineKeyboardButton(strings["en_text"], callback_data="lang:en"),
        InlineKeyboardButton(strings["fa_text"], callback_data="lang:fa")
        ]])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['choice_lang'], reply_markup=options)
