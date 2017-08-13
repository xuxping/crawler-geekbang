# -*- coding:utf-8 -*-
import json
from pymongo import MongoClient
import jieba
import sys
import re
import jieba
mcoll = MongoClient("127.0.0.1", 27017)['geek']


def segs():
    """文章分词"""
    segs_list = {}
    patter = re.compile(r'^[0-9]')
    for record in mcoll['article'].find({}, {"content": 1}):
        content = record['content'].encode('utf-8')
        segs = jieba.cut(content, cut_all=False)

        for seg in segs:
            seg = seg.replace('\r', '').replace('\n', '')
            if len(seg) < 2 or patter.match(seg):
                continue
            segs_list.setdefault(seg, 0)
            segs_list[seg] += 1
    segs_list = sorted(segs_list.items(),lambda x,y:cmp(x[1],y[1]),reverse=True)
    mcoll['statistics'].update(
        {"_id": "segs"}, {"$set": {"list": segs_list[:1000]}}, upsert=True)


def author_index():
    """作者分析"""
    authors_list = {}
    for record in mcoll['article'].find():
        # print record['_id']
        # cnt = record['content'].encode('utf-8').decode("utf-8")
        author = record['author'].encode('utf-8')
        if len(author) < 2 or author[0] == "2":
            continue

        if author not in authors_list:
            authors_list[author] = {"page_num": 0, "ids": []}
        authors_list[author]['page_num'] += 1
        if record['_id'] not in authors_list[author]['ids']:
            authors_list[author]['ids'].append(record['_id'])

    # mcoll['author_index'].save(authors_list)
    records = []
    for author, item in authors_list.iteritems():
        records.append({
            "author": author,
            "page_num": item['page_num'],
            "ids": item['ids']
        })

    mcoll['statistics'].update(
        {"_id": "authors"}, {"$set": {"list": records}}, upsert=True)


def classfiy():
    """分类"""
    classfiys = {}
    for doc in mcoll['article'].find():
        res = doc['resource'].encode('utf-8')
        if res:
            classfiys.setdefault(res, 0)
            classfiys[res] += 1

    classfiys = sorted(classfiys.items(), lambda x,
                       y: cmp(x[1], y[1]), reverse=True)
    # print classfiys
    for item in classfiys:
        print item[0], item[1]
    save_data = {
        "pdate": "20170812",
        "data_list": list(classfiys)
    }
    print save_data
    try:
        mcoll['statistics'].update({"_id": "article_classfiy"}, {
                                   "$set": save_data}, upsert=True)
    except Exception as e:
        print e


def article_publish_date():
    result = mcoll['article'].aggregate([{
        "$group": {
            "_id": "$publish_date",
            "sum": {
                "$sum": 1
            },
        }
    }])

    data_list = {}
    for doc in result:
        _id = "".join(doc['_id'].split("-"))
        if _id:
            data_list[_id] = doc['sum']
        # data_list.append((doc['_id'],doc['sum']))
    # data_list = list(result)
    data_list = sorted(data_list.items(), lambda x,
                       y: cmp(x[0], y[0]), reverse=True)

    print data_list
    save_data = {
        "pdate": "20170812",
        "data_list": data_list
    }

    try:
        mcoll['statistics'].update({"_id": "article_date"}, {
                                   "$set": save_data}, upsert=True)
    except Exception as e:
        print e


def get_all_title():
    # for doc in
    # mcoll['article'].find({"publish_date":{"$gt":"2016-00-00","$lt":"2017-00-00"}},{"title":1,"publish_date":1}):
    for doc in mcoll['article'].find({"publish_date": {"$lt": "2016-00-00"}}, {"title": 1, "publish_date": 1}):
        print doc['title'].encode('utf-8')


if __name__ == '__main__':
    # get_all_title()
    segs()
