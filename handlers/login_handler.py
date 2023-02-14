from utils.user import user_redis, create_key_button


from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

from cache.cache_session import (
    set_position,
    set_cache,
    set_login,
    set_token
)
from handlers.menu_handler import menu
from api.auth import send_data_for_login
from handlers.error_handler import error_normal, error_incorrect_data_in_login

@user_redis
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    options = ReplyKeyboardMarkup([[KeyboardButton(strings["share_phonenumber"], request_contact=True)],[KeyboardButton(strings["s_menu"])]], resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['get_phonenumber'] ,reply_markup=options)
    set_position(update.effective_chat.id, 'login:phonenumber', db)

@user_redis
async def login_get_phonenumber(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    if user['pos'] != 'login:phonenumber':
        return
    
    phone_number = update.message.text
    if phone_number == None:
        phone_number = update.message.contact.phone_number

    data = {'login':{'phone_number':phone_number}}
    set_cache(update.effective_chat.id , data, db)
    
    login_wait_for_get_password(update, context)


@user_redis
async def login_wait_for_get_password(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):
    
    options = InlineKeyboardMarkup([[
            InlineKeyboardButton(strings["register_edit_phonenumber"], callback_data='login_edit_phonenumber'),
            InlineKeyboardButton(strings["main_menu"], callback_data='main_menu')
            ]])
    
    set_position(update.effective_chat.id, 'login:password', db)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['login_get_password'] ,reply_markup=options)

    
@user_redis
async def login_get_passowrd(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):
    
    password = update.message.text
    phonenumber = user['cache']['login']

    resp, code = send_data_for_login(phonenumber, password)

    if code != 200:
        if resp == 1009:
            await error_incorrect_data_in_login(update, context)
        else:
            await error_normal(update, context)
        
        return
    
    # get info user and check tel_id , if tel id is not match , raise error
    # set token for login
    
    set_login(update.effective_chat.id, db)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['login_successfull'])       
    await menu(update, context)

