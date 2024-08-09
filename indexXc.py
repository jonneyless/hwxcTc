import math
import threading
import time

import db
import db_redis
import helpp
import net
from assist import get_current_time, get_text, get_btns, get_confirm

thread_num = 8


class Police(threading.Thread):
    def __init__(self, threadName, type, officeTgId, noticeId, items):
        super(Police, self).__init__()
        self.threadName = threadName
        self.type = type
        self.officeTgId = officeTgId
        self.noticeId = noticeId
        self.items = items

    def run(self):
        if self.type == 'delete':
            for cid in self.items:
                for uid in self.items[cid]:
                    msgIds = self.items[cid][uid]

                    chatId = int(cid)
                    userId = int(uid)

                    bot_url = helpp.get_bot_url(chatId)

                    flag, description = net.deleteMessagesWrap(bot_url, chatId, msgIds)
                    for msgId in msgIds:
                        if flag:
                            db.message_delete(chatId, msgId)
                        db.log_delete_save(chatId, userId, msgId, "hwxc delete", self.officeTgId)
        elif self.type == 'kick':
            failed = ""
            for userId in self.items:
                groups = db.user_group_get(userId)
                for group in groups:
                    bot_url = helpp.get_bot_url(group['group_tg_id'])
                    flag, description = net.banChatMemberWrap(bot_url, group['group_tg_id'], userId)
                    if flag is None:
                        failed += "%s - %s\n" % (group['group_tg_id'], userId)
                    else:
                        db.user_group_new_update(group['group_tg_id'], userId, 2, 2, 1, 2)

            if failed != "":
                helpp.sendMessage(self.officeTgId, "这些踢出操作失败，请检查：\n" + failed)


def PoliceStation(data):
    type = data['type']
    officeTgId = data['official']
    noticeId = data['notice_id']
    notice = data['notice']
    items = data['data']
    userIds = data['userIds']

    perChunk = math.ceil(len(items) / thread_num)

    chunk = []

    if type == 'delete':
        chunkData = {}
        for groupId in items:
            if len(chunkData) < perChunk:
                chunkData[groupId] = items[groupId]
            else:
                chunk.append(chunkData)

                chunkData = {groupId: items[groupId]}

        chunk.append(chunkData)
    elif type == 'kick':
        for i in range(0, len(items), perChunk):
            chunk.append(items[i:i + perChunk])

    threads = []
    i = 0
    for chunkItems in chunk:
        i = i + 1
        threads.append(Police("thread %s" % i, type, officeTgId, noticeId, chunkItems))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    if type == 'delete':
        helpp.editMessageText(officeTgId, noticeId, notice + "已完成")

        msg = "是否要将这些用户踢出所有群，并加入黑名单和骗子库：\n"
        for userId in userIds:
            msg += '[' + userId + "]\n"

        helpp.sendMessage(officeTgId, msg, get_confirm())
    elif type == 'kick':
        helpp.editMessageText(officeTgId, noticeId, "已加入骗子库，并从所有群中踢出。")


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


def checkUserId(user_tg_id):
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
    return text

if __name__ == '__main__':
    while True:
        data = db_redis.hwxcData_get()
        if data is not None:
            if 'type' in data:
                PoliceStation(data)
            else:
                ope_user_tg_id = data["ope_user_tg_id"]
                ope_msg_tg_id = data["ope_msg_tg_id"]

                user_tg_id = data["user_tg_id"]
                username = data["username"]
                fullname = data["fullname"]
                group_tg_ids = data["group_tg_ids"]

                text = checkUserId(user_tg_id)

                if len(text) > 0:
                    helpp.editMessageText(ope_user_tg_id, ope_msg_tg_id, text)
                else:
                    main(ope_user_tg_id, user_tg_id, group_tg_ids)
                    helpp.editMessageText(ope_user_tg_id, ope_msg_tg_id, get_text(user_tg_id, username, fullname, group_tg_ids), get_btns(user_tg_id))
        else:
            print("sleep 1, %s" % get_current_time())
            time.sleep(1)
    
    