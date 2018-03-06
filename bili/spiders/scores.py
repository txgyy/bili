# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ScoresItem, VideoItem
from bili.loaders import ScoresItemLoader
import datetime
from scrapy.exceptions import CloseSpider


class ScoresSpider(scrapy.Spider):
    name = 'scores'
    allowed_domains = ['www.bilibili.com', 'api.bilibili.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'bili.pipelines.BiliPipeline': None,
            'bili.pipelines.ScoresRedisPipeline': 300,
        },
        'LOG_FILE': r'logs\scores.log',
    }

    def __init__(self, pl, ks, vs):
        super(ScoresSpider, self).__init__()
        self.pl = pl
        self.ks = ks
        self.vs = vs
        self.ps = ['bangdan', 'pinlv', 'jiange', 'fenqv']
        self.start_urls = ['https://www.bilibili.com/index/rank/{:s}-{:s}{:d}-{:d}.json'.format(*self.vs)]

    def parse(self, response):
        l = ScoresItemLoader()
        rank_list = json.loads(response.body_as_unicode())['rank']['list']
        if not rank_list:
            raise CloseSpider
        for video in rank_list:
            for ix, key in enumerate(self.ps):
                l.add_value(key, self.ks[ix])
            for key in ScoresItem.fields.keys():
                if key == 'duration':
                    l.add_value(key, datetime.timedelta(**dict(zip(('minutes', 'seconds'), map(lambda x: int(x), video.get(key, '0:0').split(':'))))))
                elif key == 'dt':
                    l.add_value(key, datetime.datetime.now())
                else:
                    l.add_value(key, video.get(key))
            if self.pl:
                yield scrapy.Request('https://api.bilibili.com/x/web-interface/archive/stat?aid={}'.format(video.get('aid')),
                                     meta={'item': {'pts': video.get('pts'), }},
                                     callback=self.video_parse,
                                     )
        yield l.load_item()

    def video_parse(self, response):
        item = VideoItem()
        j = json.loads(response.body_as_unicode())['data']
        if not j:
            return
        for key in VideoItem.fields.keys():
            if key == 'dt':
                item[key] = [datetime.datetime.now()]
            elif key in response.meta.get('item').keys():
                item[key] = [response.meta.get('item').get(key)]
            else:
                item[key] = [j.get(key)]
        yield item
