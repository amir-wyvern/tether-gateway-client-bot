from utils.user import user_redis, create_key_button


from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

from cache.cache_session import (
    set_position,
    set_cache,
    set_token,
    get_token,
    get_referal_link,
    set_login
)
from handlers.menu_handler import menu
from handlers.error_handler import (
    error_user_already_exist,
    error_wrong_auth_code,
    error_number_phone_not_verified,
    error_in_registering,
    error_phone_number_already_exist,
    error_referal_link_invalid,
    error_normal
)
from api.auth import (
    send_phonenumber,
    send_auth_code,
    send_data_for_register
)
from time import time

@user_redis
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    options = ReplyKeyboardMarkup([[KeyboardButton(strings["share_phonenumber"], request_contact=True)],[KeyboardButton(strings["s_menu"])]], resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['get_phonenumber'] ,reply_markup=options)
    set_position(update.effective_chat.id, 'register:phonenumber', db)

@user_redis
async def register_phonenumber(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    if user['pos'] != 'register:phonenumber':
        return
    
    phone_number = update.message.text
    if phone_number == None:
        phone_number = update.message.contact.phone_number

    resp , code = send_phonenumber(phone_number)
    
    if code != 200:
        if resp == 1005:
            
            await error_user_already_exist(update, context)
        
        else:
            await error_normal(update, context)
            
        return

    data = {'register':{'phone_number':phone_number},'time_auth_code':time()}
    set_token(update.effective_chat.id, resp, db)
    set_cache(update.effective_chat.id , data, db)
    set_position(update.effective_chat.id, 'register:auth_code', db)

    options = InlineKeyboardMarkup([[
            InlineKeyboardButton(strings["register_edit_phonenumber"], callback_data='register_edit_phonenumber'),
            InlineKeyboardButton(strings["register_resend_auth_code"], callback_data='register_resend_auth_code'),
            InlineKeyboardButton(strings["main_menu"], callback_data='main_menu')
            ]])    
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['waiting_for_auth_code'] ,reply_markup=options)

@user_redis
async def register_resend_auth_code(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):
    
    if time() - int(user['cache']['time_auth_code'] ) < 120:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['early_request_code'] )
        return
    
    resp , code = send_phonenumber(user['cache']['register']['phone_number'])
    
    if code != 200:
        if resp == 1005:
            await error_user_already_exist(update, context)
        
        else:
            await error_normal(update, context)
            
        return
    
    set_token(update.effective_chat.id, resp, db)
    set_position(update.effective_chat.id, 'register:auth_code', db)

    options = InlineKeyboardMarkup([[
            InlineKeyboardButton(strings["register_edit_phonenumber"], callback_data='register_edit_phonenumber'),
            InlineKeyboardButton(strings["register_resend_auth_code"], callback_data='register_resend_auth_code'),
            InlineKeyboardButton(strings["main_menu"], callback_data='main_menu')
            ]])    
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['waiting_for_auth_code'] ,reply_markup=options)


@user_redis
async def regsiter_auth_code(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):
    
    # check with server
    auth_code = update.message.text
    token = get_token(update.effective_chat.id, db)
    resp, code = send_auth_code(auth_code, token)
    
    if code != 200:
        if resp == 1012:
            await error_wrong_auth_code(update, context)

        else:
            await error_normal(update, context)

    set_token(update.effective_chat.id, resp, db)

    await register_wait_for_get_name(update, context)



@user_redis
async def register_wait_for_get_name(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    options = InlineKeyboardMarkup([[
        InlineKeyboardButton(strings["main_menu"], callback_data='main_menu')
        ]])
    
    set_position(update.effective_chat.id, 'register:getname', db)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['register_get_name'] ,reply_markup=options)

@user_redis
async def register_get_name(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):
    
    name = update.message.text
    user['cache']['register']['name'] = name

    set_cache(update.effective_chat.id , user['cache'], db)

    await register_wait_for_get_lastname(update, context)

@user_redis
async def register_wait_for_get_lastname(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):
    
    options = InlineKeyboardMarkup([[
        InlineKeyboardButton(strings["back"], callback_data='register_wait_for_get_name'),
        InlineKeyboardButton(strings["main_menu"], callback_data='main_menu')
        ]])
    
    set_position(update.effective_chat.id, 'register:get_lastname', db)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['register_get_lastname'] ,reply_markup=options)

@user_redis
async def register_get_lastname(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):
    
    lastname = update.message.text
    user['cache']['register']['lastname'] = lastname

    set_cache(update.effective_chat.id , user['cache'], db)

    await register_wait_for_get_password(update, context)
    

@user_redis
async def register_wait_for_get_password(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    options = InlineKeyboardMarkup([[
        InlineKeyboardButton(strings["back"], callback_data='register_wait_for_get_lastname'),
        InlineKeyboardButton(strings["main_menu"], callback_data='main_menu')
        ]])
    
    set_position(update.effective_chat.id, 'register:get_password', db)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['register_get_password'] ,reply_markup=options)
    
@user_redis
async def register_get_password(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):
    
    password = update.message.text
    user['cache']['register']['password'] = password

    set_cache(update.effective_chat.id , user['cache'], db)
    await send_register_request(update, context)

@user_redis
async def send_register_request(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    # send to server and check register
    data = user['cache']['register']
    data.update({'tel_id':update.effective_chat.id})
    ref = get_referal_link(update.effective_chat.id, db)

    if ref:
        data.update({'referal_link': ref})

    print(data)

    token = get_token(update.effective_chat.id, db)
    resp, code = send_data_for_register(data, token)

    if code != 200:
        if resp == 1013:
            await error_number_phone_not_verified(update, context)
        if resp == 1005:
            await error_user_already_exist(update, context)
        if resp == 1006:
            await error_phone_number_already_exist(update, context)
        if resp == 1008:
            await error_referal_link_invalid(update, context)
        if resp == 1010:
            await error_in_registering(update, context)
        else:
            await error_normal(update, context)
        
        return
    
    set_login(update.effective_chat.id, db)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['register_successfull'])       
    await menu(update, context)
