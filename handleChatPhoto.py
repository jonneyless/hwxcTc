import queue
import threading
import time

import db
import db_redis
import helpp
from assist import get_current_time

thread_num = 10


def Worker():
    while True:
        data = q.get()
        if data is None:
            break

        if not helpp.updateChatPhoto(data['groupId'], data['photo']):
            q.put(data)

        q.task_done()


if __name__ == '__main__':
    while True:
        data = db_redis.updateChatPhoto()
        if data is not None:
            operatorId = data['operatorId']
            noticeId = data['noticeId']
            photo = data['photo']

            q = queue.Queue()

            threads = []
            for i in range(thread_num):
                t = threading.Thread(target=Worker)
                t.start()
                threads.append(t)

            groupIds = db.getGroupIds()
            for groupId in groupIds:
                q.put({'photo': photo, 'groupId': groupId})

            q.join()

            for i in range(thread_num):
                q.put(None)
            for t in threads:
                t.join()

            helpp.editMessageText(operatorId, noticeId, "已更新 %s 个群头像" % len(groupIds))

        else:
            print("sleep 1, %s" % get_current_time())
            time.sleep(5)
