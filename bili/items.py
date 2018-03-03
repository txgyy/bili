# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndexGlobalItem(scrapy.Item):
    # define the fields for your item here like:
    badge =scrapy.Field()
    cover = scrapy.Field()
    favorites = scrapy.Field()
    is_finish = scrapy.Field()
    newest_ep_index = scrapy.Field()
    pub_string = scrapy.Field()
    pub_time = scrapy.Field()
    season_id = scrapy.Field()
    season_status = scrapy.Field()
    title = scrapy.Field()
    total_count = scrapy.Field()
    update_pattern = scrapy.Field()
    update_time = scrapy.Field()
    url = scrapy.Field()
    week = scrapy.Field()

class ScoresItem(scrapy.Item):
    dt = scrapy.Field()
    aid = scrapy.Field()
    coins = scrapy.Field()
    play = scrapy.Field()
    video_review = scrapy.Field()
    bangdan = scrapy.Field()
    pinlv = scrapy.Field()
    jiange = scrapy.Field()
    fenqv = scrapy.Field()
    author = scrapy.Field()
    duration = scrapy.Field()
    mid = scrapy.Field()
    pic = scrapy.Field()
    pts = scrapy.Field()
    title = scrapy.Field()
    trend = scrapy.Field()

class VideoItem(scrapy.Item):
    dt = scrapy.Field()
    pts = scrapy.Field()
    aid = scrapy.Field()
    view = scrapy.Field()
    danmaku = scrapy.Field()
    reply = scrapy.Field()
    favorite = scrapy.Field()
    coin = scrapy.Field()
    share = scrapy.Field()
    now_rank = scrapy.Field()
    his_rank = scrapy.Field()
    no_reprint = scrapy.Field()
    copyright = scrapy.Field()