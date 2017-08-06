# -*- coding:utf-8 -*-
import requests
import json
from pymongo import MongoClient
import hashlib
url = "http://search.geekbang.org/searchmore?q=&t=0&s=&size=20&p=1&o=3"
mcoll = MongoClient("127.0.0.1", 27017)['geek']['links']

def save_to_mongo(records):
    for record in records:
        __m_hash = hashlib.md5()
        __m_hash.update(record['url'])
        _id = __m_hash.hexdigest()
        mcoll.update({"_id": _id}, {"$set": record},upsert=True)


for m in range(0, 12):
    for t in (0,2,5):
        totalPages = 2
        now_page = 0
        while now_page < totalPages:
            now_page += 1
            post_data = "q=&t=%s&s=&size=40&p=%s&o=%s" % (t,now_page, m)
            url = "http://search.geekbang.org/searchmore?%s" % post_data
            print url
            try:
                req = requests.post(url=url)
            except:
                print "error %s" % url
                continue
            req.encoding = "utf-8"
            data = json.loads(req.text)
            save_to_mongo(data['result']['content'])
            totalPages = data['result']['totalPages']
       
