import json

import redis

from config import redisInfo

redis_host = redisInfo['host']
redis_port = redisInfo['port']

pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=1)
pool11 = redis.ConnectionPool(host=redis_host, port=redis_port, db=11)
pool10 = redis.ConnectionPool(host=redis_host, port=redis_port, db=10)
prefix = "welcome_"

# ==========================================================================================================================================

def get_conn():
    return redis.Redis(connection_pool=pool)

def get_conn10():
    return redis.Redis(connection_pool=pool10)


def get_conn11():
    return redis.Redis(connection_pool=pool11)
    

# ==========================================================================================================================================

def db_log_get():
    key = "qunguanAdmin_" + "db_log_qq"
    
    conn = get_conn10()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def db_log_set(data):
    key = "qunguanAdmin_" + "db_log_qq"

    conn = get_conn10()

    conn.rpush(key, json.dumps(data))


def hwxcData_get():
    key = prefix + "hwxcData_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def hwxcData_xc_get():
    key = prefix + "hwxcData_xc_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def hwxcData_xc_len():
    key = prefix + "hwxcData_xc_qq"
    
    conn = get_conn()

    return conn.llen(key)


# ---------------------------------------------------------------------------

def bot_url_get(group_tg_id, typee):
    key = prefix + "bot_url_new" + str(group_tg_id) + str(typee)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return str(val, encoding="utf-8")


def bot_url_set(group_tg_id, typee, bot_url):
    key = prefix + "bot_url_new" + str(group_tg_id) + str(typee)
    
    conn = get_conn()
    
    conn.set(key, bot_url, 300)  # 5分钟


def updateChatPhoto(data=None):
    key = prefix + ":chat:photo:update"

    conn = get_conn()

    if data is not None:
        conn.rpush(key, json.dumps(data))
        return

    val = conn.lpop(key)
    if val is None:
        return None
    else:
        return json.loads(val)


def getFakeGroupIds():
    key = prefix + ":fakeGroupIds"

    conn = get_conn11()

    return conn.hkeys(key)


def getBotTokenByFakeGroupId(group_id):
    key = prefix + ":fakeGroupIds"

    conn = get_conn11()

    return conn.hget(key, group_id)


def removeFakeGroupId(groupId):
    key = prefix + ":fakeGroupIds"

    conn = get_conn11()

    conn.hdel(key, groupId)
