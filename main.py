import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)

from dotenv import load_dotenv
import os
from pathlib import Path

from utils.user import user_redis
from handlers.start_handler import start
from handlers.message_handler import message_handler
from handlers.phonrnumber_handler import phonenumber_handler
from handlers.callback_handler import callback_handler


dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
) 

TOKEN_BOT = os.getenv('TOKEN_BOT')


# bot = Bot('5913451139:AAHrEMVN9io8WFBRCMtxH4UgM6iayywQJ78')

if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN_BOT).build()
    # application = ApplicationBuilder().token('5913451139:AAHrEMVN9io8WFBRCMtxH4UgM6iayywQJ78').build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT, message_handler))
    application.add_handler(MessageHandler(filters.CONTACT, phonenumber_handler))
    application.add_handler(CallbackQueryHandler(callback_handler))
    
    application.run_polling()
