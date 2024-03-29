# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class DangdangPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db1):
        self.mongo_url = mongo_uri
        self.mongo_db = mongo_db1

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONOGO_URL'),
            mongo_db1=crawler.settings.get('MONOGO_DB'),
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].update_one({'comment':item['comment']},{'$set':dict(item)},True)
        return item