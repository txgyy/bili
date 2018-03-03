#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy_redis.dupefilter import RFPDupeFilter
from scrapy_redis.connection import get_redis_from_settings
class ScoresRFPDupeFilter(RFPDupeFilter):
    @classmethod
    def from_settings(cls, settings):
        server = get_redis_from_settings(settings)
        key = settings.get('DUPEFILTER_KEY')
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(server, key=key, debug=debug)

    def close(self, reason=''):
        pass
