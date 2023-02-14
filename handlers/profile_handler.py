from utils.user import user_redis


from telegram import Update
from telegram.ext import ContextTypes



@user_redis
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):
    pass

