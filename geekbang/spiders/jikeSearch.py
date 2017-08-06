# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from scrapy.selector import Selector
from scrapy.http import Request
from geekbang.items import GeekbangItem


class JikesearchSpider(scrapy.Spider):
    name = "jikeSearch"
    # allowed_domains = ["s.geekbang.org"]
    # start_urls = ['http://s.geekbang.org/']

    def start_requests(self):
        mcoll = MongoClient("127.0.0.1", 27017)['jike']['links']
        for doc in mcoll.find():
            print doc['url']
            if doc['url'][:9] == 'http://mp':
                yield Request(url=doc['url'], callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        item = GeekbangItem()
        item['url'] = response.url
        try:
            title = sel.xpath(
                '//h2[@id="activity-name"]/text()').extract()[0].strip()
        except:
            title = ""
        item['title'] = title
        try:
            article_type = sel.xpath(
                '//span[@id="copyright_logo"]/text()').extract()[0].strip()
        except Exception:
            article_type = u'原创'

        item['article_type'] = article_type
        try:
            publish_date = sel.xpath(
                '//em[@id="post-date"]/text()').extract()[0].strip()
        except Exception:
            publish_date = ""
        item['publish_date'] = publish_date

        try:
            resource = sel.xpath(
                '//a[@id="post-user"]/text()').extract()[0].strip()
        except:
            resource = ""
        item['resource'] = resource

        content_wrap = sel.xpath('//div[@id="js_content"]')
        content = content_wrap.xpath('string(.)').extract()[0]
        item['content'] = content
        item['images'] = response.xpath('//img/@data-src').extract()

        yield item
