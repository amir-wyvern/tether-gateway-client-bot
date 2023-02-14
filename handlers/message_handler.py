from telegram import Update
from telegram.ext import ContextTypes


from utils.user import user_redis

from handlers.menu_handler import menu
from handlers.rules_handler import rules
from handlers.support_handler import support, get_support_message
from handlers.finacial_handler import financial
from handlers.profile_handler import profile
from handlers.contract_handler import contract
from handlers.register_handler import (
    register,
    register_get_lastname,
    register_get_name,
    register_get_password,
    register_phonenumber,
    regsiter_auth_code
)
from handlers.login_handler import (
    login_get_phonenumber,
    login_get_passowrd
)

@user_redis
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, user, strings, db):
    
    messages_pointer = {
        strings["s_register"]: lambda : register(update, context),
        strings["s_rules"] : lambda : rules(update, context),
        strings["s_support"] : lambda : support(update, context),
        strings["s_profile"] : lambda : profile(update, context),
        strings["s_financial"] : lambda : financial(update, context),
        strings["s_contract"] : lambda : contract(update, context),
        strings["s_menu"] : lambda : menu(update, context),
    }

    positions_pointer = {
        'menu': lambda : menu(update, context),
        'register:auth_code': lambda : regsiter_auth_code(update, context),
        'register:phonenumber': lambda : register_phonenumber(update, context) ,
        "support": lambda : get_support_message(update, context),
        "register:getname": lambda : register_get_name(update, context),
        "register:get_lastname": lambda : register_get_lastname(update, context),
        "register:get_password": lambda : register_get_password(update, context),
        # "login:phonenumber" : lambda : login_get_phonenumber(update, context),
        "register:get_password" : lambda : login_get_passowrd(update, context)
    }

    if update.message.text in messages_pointer:

        await messages_pointer[update.message.text]()
    
    elif user['pos'] in positions_pointer:

        await positions_pointer[user['pos']]()

