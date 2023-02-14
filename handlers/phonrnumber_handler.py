from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils.user import user_redis
from cache.cache_session import (
    set_position,
    set_cache
)
from handlers.register_handler import register_phonenumber


@user_redis
async def phonenumber_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    if user['pos'] == 'register:phonenumber':
        
        await register_phonenumber(update, context)
        
        # phone_number = update.message.contact.phone_number
        # data = {'register':{'phone_number':phone_number}}

        # set_cache(update.effective_chat.id , data, db)
        # set_position(update.effective_chat.id, 'register:auth_code', db)

        # options = InlineKeyboardMarkup([[
        #         InlineKeyboardButton(strings["register_edit_phonenumber"], callback_data='register_edit_phonenumber'),
        #         InlineKeyboardButton(strings["main_menu"], callback_data='main_menu')
        #         ]])    
        
        # await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['waiting_for_auth_code'] ,reply_markup=options)

    elif user['pos'] == 'login:phonenumber':
        
        phone_number = update.message.contact.phone_number
        data = {'register':{'phone_number':phone_number}}

        set_cache(update.effective_chat.id , data, db)
        set_position(update.effective_chat.id, 'register:auth_code', db)

        options = InlineKeyboardMarkup([[
                InlineKeyboardButton(strings["register_edit_phonenumber"], callback_data='register_edit_phonenumber'),
                InlineKeyboardButton(strings["main_menu"], callback_data='main_menu')
                ]])    
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['waiting_for_auth_code'] ,reply_markup=options)
