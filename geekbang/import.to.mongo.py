# -*- coding: utf-8 -*-
from pymongo import MongoClient
import hashlib
import json
import time


def my_md5(str):
    _md5 = hashlib.md5()
    _md5.update(str)
    return _md5.hexdigest()


class JsonPipeline():
    def __init__(self):
        mongo_client = MongoClient('127.0.0.1', 27017)
        self._mcoll = mongo_client['jike']['article']
        self.pdate = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

    def process_item(self, item):
        # _item = dict(item)
        _item['_id'] = my_md5(item['url'])
        _item['pdate'] = self.pdate[:8]

        self._mcoll.save(_item)

    def save_to_db(self):
        with open(name="./weixin.json", mode='r') as fp:
            for line in fp :
                try:
                    record = json.loads(line)
                except:
                    continue
                else:
                    print record['resource']


if __name__ == '__main__':
    proccess = JsonPipeline()
    proccess.save_to_db()
