from cache.database import AUTH_TOKEN_EXPIRE
import redis
import json

def create_auth_session(token, value, db: redis.Redis):
    return db.set(token, value, ex= AUTH_TOKEN_EXPIRE)

def get_auth_session(token: str, db: redis.Redis):

    return db.get(token)

def get_user(tel_id, item, db: redis.Redis):

    if item == 'all':
        resp = db.hgetall(f'tel_id:{tel_id}')
        if resp == {}:
            resp = None
        
        # if resp['cache'] != {}
        return resp
    
    else:
        return db.hget(f'tel_id:{tel_id}', item)
    
def set_new_user(tel_id, db: redis.Redis)-> dict:

    data = {
        'token': 'None',
        'login': 'not logined',
        'pos':'menu',
        'tel_id': tel_id,
        'lang': 'en',
        'cache': json.dumps({})
    }

    db.hset(f'tel_id:{tel_id}', mapping= data)
    return data

def set_lang(tel_id, lang, db:redis.Redis):

    db.hset(f'tel_id:{tel_id}', 'lang', lang)
    return lang

def set_position(tel_id, pos, db:redis.Redis):

    db.hset(f'tel_id:{tel_id}', 'pos', pos)
    return pos

def set_cache(tel_id, data, db:redis.Redis):

    db.hset(f'tel_id:{tel_id}', 'cache', json.dumps(data))
    return data

def get_cache(tel_id, db:redis.Redis):

    data = db.hget(f'tel_id:{tel_id}', 'cache')
    return json.loads(data)

def set_login(tel_id, db:redis.Redis):

    db.hset(f'tel_id:{tel_id}', 'login', True)
    return True

def set_token(tel_id, token, db: redis.Redis):
    
    db.hset(f'tel_id:{tel_id}', 'token', token)
    return token

def get_token(tel_id, db: redis.Redis):
    
    data = db.hget(f'tel_id:{tel_id}', 'token')
    return data

def set_referal_link(tel_id, ref, db: redis.Redis):

    db.set(f'ref:tel_id:{tel_id}', ref)
    return ref

def get_referal_link(tel_id, db: redis.Redis):

    ref = db.get(f'ref:tel_id:{tel_id}')
    db.delete(f'ref:tel_id:{tel_id}')
    return ref

def set_login(tel_id, db: redis.Redis):

    db.set(f'ref:tel_id:{tel_id}', 'login', 'logined')
    return True