from telegram import ReplyKeyboardMarkup
import json

from utils.tel import create_key_button
from cache.database import get_redis_cache
from languege.lang import loadLange 
from cache.cache_session import (
    get_user,
    set_new_user
)

lang = loadLange()

def user_redis(func):
  
    async def wrapper(*args, **kwargs):
        # try:
            tel_id = args[0].effective_chat.id
            db = get_redis_cache().__next__()
            user = get_user(tel_id, 'all',db)
            if user is None:
                user = set_new_user(tel_id, db)

            user['cache'] = json.loads(user['cache'])

            kwargs.update({
                'db': db,
                'user': user,
                'strings': getattr(lang, user['lang'])
                })
            
            result = await func(*args, **kwargs)
            return result

        # except:
        #     ls = create_key_button(kwargs["strings"]["key_problem"])
        #     options =ReplyKeyboardMarkup(ls , resize_keyboard=True)
        #     await args[1].bot.send_message(chat_id=args[0].effective_chat.id, text=kwargs["strings"]['problem'], reply_markup=options)

    return wrapper

