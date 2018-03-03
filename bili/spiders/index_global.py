# -*- coding: utf-8 -*-
import scrapy
from ..items import IndexGlobalItem
from scrapy.loader import ItemLoader
import json
import datetime
class IndexGlobalSpider(scrapy.Spider):
    name = 'index_global'
    allowed_domains = ['bangumi.bilibili.com']
    start_urls = [
        'https://bangumi.bilibili.com/web_api/season/index_global?page={page:d}&page_size=20&version=0&is_finish=0&start_year=0&tag_id=&index_type=1&index_sort=0&quarter=0'
    ]
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS':{
            'Host':'bangumi.bilibili.com',
            'Referer':'https://bangumi.bilibili.com/anime/index',
        }
    }
    def __init__(self,**kwargs):
        super(IndexGlobalSpider,self).__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url.format(page=1),meta={'flag':True,})

    def parse(self, response):
        result =json.loads(response.body_as_unicode()).get('result')
        l = ItemLoader(item=IndexGlobalItem())
        for anime in result['list']:
            for key in IndexGlobalItem.fields.keys():
                if key=='pub_time':
                    l.add_value(key,datetime.date.fromtimestamp(anime.get(key)) if anime.get(key)>=0 else datetime.date.fromtimestamp(0)+datetime.timedelta(seconds=anime.get(key)))
                elif key=='update_time':
                    l.add_value(key,datetime.datetime.fromtimestamp(anime.get(key))if anime.get(key)>=0 else datetime.datetime.fromtimestamp(0)+datetime.timedelta(seconds=anime.get(key)))
                else:
                    l.add_value(key,anime.get(key,''))
        yield l.load_item()

        if response.meta.get('flag'):
            for page in range(2,int(result['pages'])+1):
                yield scrapy.Request(url=self.start_urls[0].format(page=page),meta={'flag':False,})
