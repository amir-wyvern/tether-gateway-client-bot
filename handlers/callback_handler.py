from telegram.ext import ContextTypes
from telegram import Update

from handlers.menu_handler import menu
from handlers.languege_handler import select_lang
from handlers.register_handler import (
    register,
    register_wait_for_get_lastname,
    register_wait_for_get_name,
    register_resend_auth_code

)
from handlers.login_handler import (
    login
)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query
    chat_id = query.message.chat.id

    await query.answer()

    callback_posiner = {
        'main_menu': lambda : menu(update, context),
        'register_edit_phonenumber': lambda : register(update, context),
        # 'login_edit_phonenumber': lambda : login(update, context),
        'lang': lambda : select_lang(update, context),
        "register_wait_for_get_name": lambda : register_wait_for_get_name(update, context),
        "register_wait_for_get_lastname": lambda : register_wait_for_get_lastname(update, context),
        "register_resend_auth_code" : lambda : register_resend_auth_code(update, context)
    }

    key = query.data.split(':')[0]

    if key in callback_posiner:
        await callback_posiner[key]()