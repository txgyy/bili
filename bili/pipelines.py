# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import VideoItem, ScoresItem, IndexGlobalItem
from .models import Session, IndexGlobalModel, VideoModel, ScoresModel
from scrapy_redis.pipelines import RedisPipeline


class BiliPipeline(object):
    def __init__(self, MYSQL_URL):
        self.MYSQL_URL = MYSQL_URL

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            MYSQL_URL=crawler.settings.get('MYSQL_URL'),
        )

    def open_spider(self, spider):
        self.session = Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        model = globals().get(item.__class__.__name__[:-4] + 'Model')
        try:
            self.insert(model, item)
            # self.session.execute(model.__table__.insert().prefix_with('ignore'), list(map(lambda v: dict(zip(item._values.keys(), v)), zip(*item._values.values(), ))))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)
        return item

    def update(self, model, item):
        self.session.bulk_update_mappings(model, map(lambda v: dict(zip(item.keys(), v)), zip(*item.values(), )))

    def insert(self, model, item):
        self.session.bulk_insert_mappings(model, map(lambda v: dict(zip(item.keys(), v)), zip(*item.values(), )))


class ScoresRedisPipeline(RedisPipeline):
    def _process_item(self, item, spider):
        key = self.item_key(item, spider)
        data = map(lambda v: self.serialize(dict(zip(item.keys(), v))), zip(*item.values(), ))
        self.server.rpush(key, *data)
        return item

    def item_key(self, item, spider):
        return self.key % {'item': item.__class__.__name__}
