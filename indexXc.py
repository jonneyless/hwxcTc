import threading
import time

import db
import db_redis
import net
import helpp
import math
from assist import get_current_time, get_text, get_btns

thread_num = 8


class MyThread(threading.Thread):
    def __init__(self, threadName, ope_user_tg_id, user_tg_id, group_tg_ids):
        super(MyThread, self).__init__()
        self.threadName = threadName
        self.ope_user_tg_id = ope_user_tg_id
        self.user_tg_id = user_tg_id
        self.group_tg_ids = group_tg_ids
        
    def run(self):
        threadName = self.threadName
        ope_user_tg_id = self.ope_user_tg_id
        user_tg_id = self.user_tg_id
        group_tg_ids = self.group_tg_ids

        for group_tg_id in group_tg_ids:
            bot_url = helpp.get_bot_url(group_tg_id)
            
            flag, description = net.banChatMemberWrap(bot_url, group_tg_id, user_tg_id)
            db.log_kick_save(group_tg_id, user_tg_id, "hwxc kick", ope_user_tg_id)
            db.user_group_new_update(group_tg_id, user_tg_id, 2, 2, 1, 2)

            msg_tg_ids = db.msg48_get(group_tg_id, user_tg_id)
            msg_tg_ids_len = len(msg_tg_ids)
            if msg_tg_ids_len > 0:
                temp = 1
                temp_max = math.ceil(msg_tg_ids_len / 100)
                
                while temp <= temp_max:
                    start = (temp - 1) * 100
                    end = start + 100
                    
                    msg_tg_ids100 = msg_tg_ids[start:end]
                        
                    temp = temp + 1
                    
                    flag, description = net.deleteMessagesWrap(bot_url, group_tg_id, msg_tg_ids100)
                    for msg_tg_id in msg_tg_ids100:
                        if flag:
                            db.message_delete(group_tg_id, msg_tg_id)
                        db.log_delete_save(group_tg_id, user_tg_id, msg_tg_id, "hwxc delete", ope_user_tg_id)
            
                
def main(ope_user_tg_id, user_tg_id, group_tg_ids):
    groups_len = len(group_tg_ids)
    single_len = math.ceil(groups_len / thread_num)
    
    arr = []
    arr_temp = []
    
    for group_tg_id in group_tg_ids:
        if len(arr_temp) < single_len:
            arr_temp.append(group_tg_id)
        else:
            arr.append(arr_temp)

            arr_temp = []
            arr_temp.append(group_tg_id)
            
    if len(arr_temp) > 0:
        arr.append(arr_temp)

    arr_len = len(arr)
    
    threads = []
    for i in range(arr_len):
        threads.append(MyThread("thread %s" % i, ope_user_tg_id, user_tg_id, arr[i]))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    while True:
        data = db_redis.hwxcData_get()
        if data is not None:
            ope_user_tg_id = data["ope_user_tg_id"]
            ope_msg_tg_id = data["ope_msg_tg_id"]
            
            user_tg_id = data["user_tg_id"]
            username = data["username"]
            fullname = data["fullname"]
            group_tg_ids = data["group_tg_ids"]
            
            text = ""
            official = db.official_one(user_tg_id)
            if official is not None:
                text = "尝试操作的用户 %s 为官方账号，无法将其添加到黑名单，请核对后重新操作" % user_tg_id
            else:
                white = db.white_one(user_tg_id)
                if white is not None:
                    text = "尝试操作的用户 %s 为白名单账号，无法将其添加到黑名单，请核对后重新操作" % user_tg_id
                else:
                    admin = db.admin_one(user_tg_id)
                    if admin is not None:
                        text = "尝试操作的用户 %s 为群管理，无法将其添加到黑名单，请核对后重新操作" % user_tg_id

            if len(text) > 0:
                helpp.editMessageText(ope_user_tg_id, ope_msg_tg_id, text)
            else:
                main(ope_user_tg_id, user_tg_id, group_tg_ids)
                helpp.editMessageText(ope_user_tg_id, ope_msg_tg_id, get_text(user_tg_id, username, fullname, group_tg_ids), get_btns(user_tg_id))
        else:
            print("sleep 1, %s" % get_current_time())
            time.sleep(1)
    
    