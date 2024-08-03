import threading
import time

import db
import db_redis
import net
import helpp
import math
from assist import get_current_time, get_text, get_btns, get_confirm

thread_num = 8


class MyThread(threading.Thread):
    def __init__(self, threadName, type, officeTgId, noticeId, items):
        super(MyThread, self).__init__()
        self.threadName = threadName
        self.type = type
        self.officeTgId = officeTgId
        self.noticeId = noticeId
        self.items = items

    def run(self):
        if self.type == 'delete':
            for chatId in self.items:
                for userId in self.items[chatId]:
                    msgIds = self.items[chatId][userId]

                    chatId = int(chatId)
                    userId = int(userId)

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

            if failed != "":
                helpp.sendMessage(self.officeTgId, "这些踢出操作失败，请检查：\n" + failed)



def main(data):
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
        threads.append(MyThread("thread %s" % i, type, officeTgId, noticeId, chunkItems))

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


if __name__ == '__main__':
    while True:
        data = db_redis.clearFakeMsgQueue()
        if data is not None:
            main(data)
        else:
            print("sleep 1, %s" % get_current_time())
            time.sleep(1)
