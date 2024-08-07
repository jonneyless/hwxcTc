import math
import threading
import time

import db_redis
import helpp
from assist import get_current_time

thread_num = 10


class notice(threading.Thread):
    def __init__(self, groupIds):
        super(notice, self).__init__()
        self.groupIds = groupIds

    def run(self):
        for groupId in self.groupIds:
            token = db_redis.getBotTokenByFakeGroupId(groupId)
            if helpp.sendMessageByWelcome(groupId, token, "本群是假群，请马上退群，小心上当受骗。") == 0:
                print('send to ' + str(groupId))
            else:
                db_redis.removeFakeGroupId(groupId)


def fakeGroup(groupIds):
    perChunk = math.ceil(len(groupIds) / thread_num)

    chunk = []
    for i in range(0, len(groupIds), perChunk):
        chunk.append(groupIds[i:i + perChunk])

    threads = []
    i = 0
    for chunkItems in chunk:
        i = i + 1
        threads.append(notice(chunkItems))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    while True:
        data = db_redis.getFakeGroupIds()
        if data is not None and len(data) > 0:
            fakeGroup(data)
        else:
            print("sleep 5, %s" % get_current_time())
            time.sleep(1)
