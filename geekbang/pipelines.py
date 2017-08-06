# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
from pymongo import MongoClient
import time

def my_md5(str):
    _md5 = hashlib.md5()
    _md5.update(str)
    return _md5.hexdigest()


class JsonPipeline(object):
    def __init__(self):
        mongo_client = MongoClient('127.0.0.1', 27017)
        self._mcoll = mongo_client['jike']['article']
        self.pdate = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

    def process_item(self, item, spider):
        _item = dict(item)
        _item['_id'] = my_md5(item['url'])
        _item['pdate'] = self.pdate[:8]

        self._mcoll.save(_item)
        return item
