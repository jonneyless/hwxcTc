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
            if data['retry'] < 3:
                # 上传失败就丢队列尾部重试
                data['retry'] = data['retry'] + 1
                print(str(data['groupId']) + " retry " + str(data['retry']))
                q.put(data)
            else:
                print(str(data['groupId']) + " failure ")

        q.task_done()


if __name__ == '__main__':
    while True:
        data = db_redis.updateChatPhoto()
        print('update chat photo:' + str(data['photo']))
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
                q.put({'photo': photo, 'groupId': groupId, 'retry': 0})

            q.join()

            for i in range(thread_num):
                q.put(None)
            for t in threads:
                t.join()

            helpp.editMessageText(operatorId, noticeId, "已更新 %s 个群头像" % len(groupIds))

        else:
            print("sleep 1, %s" % get_current_time())
            time.sleep(5)
