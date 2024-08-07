import db_redis
from assist import get_current_time
from dbpool import OPMysql


# ==========================================================================================================================================

def official_one(user_tg_id):
    opm = OPMysql()

    sql = "select id from offical_user where tg_id = '%s' limit 1" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


def admin_one(user_tg_id):
    opm = OPMysql()

    sql = "select id from group_admin where user_id = '%s'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
def white_one(user_tg_id):
    opm = OPMysql()

    sql = "select id from white_user where tg_id = '%s' limit 1" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
def user_group_get(user_tg_id):
    opm = OPMysql()

    sql = "select group_tg_id from user_group_new where user_tg_id = '%s'" % user_tg_id

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


def msg48_get(group_tg_id, user_tg_id):
    ids = []
    
    opm = OPMysql()

    sql = "select msg_tg_id from log_msg48 where group_tg_id = '%s' and user_tg_id = '%s' order by id desc" % (group_tg_id, user_tg_id)

    result = opm.op_select_all(sql)

    opm.dispose()
    
    if result is not None:
        for item in result:
            ids.append(int(item["msg_tg_id"]))
    
    return ids
    
    
def bot_one(group_tg_id, typee = 2):
    # typee 踢出操作机器人
    
    opm = OPMysql()

    sql = "select bots.* from bot_group join bots on bot_group.user_tg_id = bots.tg_id where bot_group.group_tg_id = '%s' and bots.type = %s" % (group_tg_id, typee)

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
# ==========================================================================================================================================

def message_delete(group_tg_id, message_tg_id):
    opm = OPMysql()

    sql = "update msg set flag = 2 where chat_id = '%s' and message_id = '%s'" % (group_tg_id, message_tg_id)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))
    
    opm.dispose()
    
    return result
    
    
def log_delete_save(group_tg_id, user_tg_id, message_tg_id, reason, admin_id):
    opm = OPMysql()

    sql = "insert into log_delete_message(group_tg_id, user_tg_id, message_tg_id, reason, created_at, admin_id) values('%s', '%s', '%s', '%s', '%s', '%s')" % (group_tg_id, user_tg_id, message_tg_id, reason, get_current_time(), admin_id)

    db_redis.db_log_set({
        "sql": sql,
    })

    # result = None
    # try:
    #     result = opm.op_update(sql)
    # except Exception as e:
    #     print("sql %s %s" % (sql, e))

    # opm.dispose()

    # return result
    
    
def log_kick_save(group_tg_id, user_tg_id, reason, admin_id):
    opm = OPMysql()

    sql = "insert into log_ban_user(group_tg_id, user_tg_id, reason, created_at, admin_id) values('%s', '%s', '%s', '%s', '%s')" % (
        group_tg_id, user_tg_id, reason, get_current_time(), admin_id)

    db_redis.db_log_set({
        "sql": sql,
    })

    # result = None
    # try:
    #     result = opm.op_update(sql)
    # except Exception as e:
    #     print("sql %s %s" % (sql, e))
    
    # opm.dispose()
    
    # return result


def user_group_new_update(group_tg_id, user_tg_id, is_admin=-1, status_in=-1, status_restrict=-1, status_ban=-1):
    opm = OPMysql()

    sql = "update user_group_new set is_admin = %s, status_in = %s, status_restrict = %s, status_ban = %s, updated_at = '%s' where group_tg_id = '%s' and user_tg_id ='%s'" % (is_admin, status_in, status_restrict, status_ban, get_current_time(), group_tg_id, user_tg_id)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result


def getGroupIds():
    opm = OPMysql()

    sql = "select chat_id from `groups` where deleted = 2 and opened = 1"

    result = opm.op_select_all(sql)

    opm.dispose()

    ids = []
    for group in result:
        ids.append(group['chat_id'])

    return ids
