#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from bili.items import ScoresItem
class ScoresItemLoader(ItemLoader):
    default_item_class = ScoresItem
    duration_in = MapCompose(str)