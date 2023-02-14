
from utils.user import user_redis, create_key_button


from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup


@user_redis
async def error_user_already_exist(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    ls = create_key_button(strings["key_problem"])
    options =ReplyKeyboardMarkup(ls , resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['already_account'], reply_markup=options)

@user_redis
async def error_in_registering(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    ls = create_key_button(strings["key_problem"])
    options =ReplyKeyboardMarkup(ls , resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['error_in_registering'], reply_markup=options)

@user_redis
async def error_referal_link_invalid(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    ls = create_key_button(strings["key_problem"])
    options =ReplyKeyboardMarkup(ls , resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['error_referal_link_invalid'], reply_markup=options)

@user_redis
async def error_phone_number_already_exist(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    ls = create_key_button(strings["key_problem"])
    options =ReplyKeyboardMarkup(ls , resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['error_phone_number_already_exist'], reply_markup=options)

@user_redis
async def error_number_phone_not_verified(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    ls = create_key_button(strings["key_problem"])
    options =ReplyKeyboardMarkup(ls , resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['error_number_phone_not_verified'], reply_markup=options)

@user_redis
async def error_normal(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    ls = create_key_button(strings["key_problem"])
    options =ReplyKeyboardMarkup(ls , resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['problem'], reply_markup=options)

@user_redis
async def error_wrong_auth_code(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    options = InlineKeyboardMarkup([[
        InlineKeyboardButton(strings["register_edit_phonenumber"], callback_data='register_edit_phonenumber'),
        InlineKeyboardButton(strings["main_menu"], callback_data='main_menu')
        ]])
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['wrong_auth_code'] ,reply_markup=options)

@user_redis
async def error_incorrect_data_in_login(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):

    options = InlineKeyboardMarkup([[
        InlineKeyboardButton(strings["register_edit_phonenumber"], callback_data='login_edit_phonenumber'),
        InlineKeyboardButton(strings["main_menu"], callback_data='main_menu')
        ]])
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=strings['incorrect_data_in_login'] ,reply_markup=options)