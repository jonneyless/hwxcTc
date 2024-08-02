import time


# ==========================================================================================================================================

def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_today_time():
    return time.strftime("%Y-%m-%d", time.localtime())


def get_today_timestamp():
    return time2timestamp(get_today_time(), False)


def get_current_timestamp():
    return int(time.time())


def time2timestamp(t, flag=True):
    if flag:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S')))
    else:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d')))


def timestamp2time(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))


def get_simple_time(created_at):
    created_at = str(created_at)
    space = created_at.find(" ")
    return created_at[(space + 1):]

    
# ==========================================================================================================================================

def get_text(user_tg_id, username, fullname, groups):
    text_basic = "用户tgid: %s\n" % user_tg_id
    text_basic += "用户名：@%s\n" % username
    text_basic += "用户昵称: %s\n" % fullname
    text_basic += "群组：%s个\n" % len(groups)
    text_basic += "正在执行：删除所有信息、踢出所在群组、加入黑名单\n"
    text_basic += "状态：<b>已完成</b>"
    
    return text_basic
    
    
def get_btns(user_tg_id):
    callback_data = "cheat?user_tg_id=%s" % user_tg_id
    
    arr = [
        [
            {
                "text": "点击加入骗子库",
                "callback_data": callback_data,
            },
        ]
    ]
    
    return {
        "inline_keyboard": arr
    }
    
    