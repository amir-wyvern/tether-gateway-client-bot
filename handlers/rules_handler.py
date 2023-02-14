from utils.user import user_redis


from telegram import Update
from telegram.ext import ContextTypes


@user_redis
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['rule_text'])
