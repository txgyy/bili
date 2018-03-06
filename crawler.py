from twisted.internet import reactor, defer,task
from scrapy.crawler import CrawlerRunner,CrawlerProcess
from scrapy.utils.project import get_project_settings
from itertools import product
from scrapy.utils.log import configure_logging
from bili.spiders.scores import ScoresSpider
from redis import StrictRedis
from datetime import datetime
from time import sleep
configure_logging()
runner = CrawlerProcess(get_project_settings())
redis = StrictRedis.from_url(get_project_settings().get('REDIS_URL'))
@defer.inlineCallbacks
def crawl(pl):
    yield redis.delete('dupefilter:timestamp')
    yield print(datetime.now().time(),': start')

    for i in get_params(pl):
        yield runner.crawl(ScoresSpider,pl, *zip(*i, ))
    yield print(datetime.now().time(),': finish')
    # reactor.stop()


def get_params(pl=True):
    bangdan = (
        ('全站', 'all',),
        ('原创', 'origin',),
        ('新人', 'rookie',),
        ('影视', 'all',),
    )
    pinlv = (
        ('全部', '',),
        ('近期', '0',),
    )
    jiange = (
        ('一日', 1,),
        ('三日', 3,),
        ('一周', 7,),
        ('一月', 30,),
    )
    fenqv = (
        ('全站', 0,),
        ('动画', 1,),
        ('音乐', 3,),
        ('舞蹈', 129,),
        ('游戏', 4,),
        ('科技', 36,),
        ('生活', 160,),
        ('鬼畜', 119,),
        ('时尚', 155,),
        ('娱乐', 5,),
        ('影视', 181,),
        ('国创相关', 168,),
        ('纪录片', 117,),
        ('电影', 23,),
        ('电视剧', 11,),
    )
    if pl:
        for i in product(bangdan[1:2], pinlv[-1:], jiange[:1], fenqv[1:-3]):
            yield i
        # 近期
        # for i in product(bangdan[:2], pinlv[-1:], jiange[:-1], fenqv[:-3]):
        #     yield i
        # for i in product(bangdan[-1:], pinlv[-1:], jiange[:-1], fenqv[-3:]):
        #     yield i
    else:
        # 全部
        for i in product(bangdan[:2], pinlv[0:-1], jiange, fenqv[:-3]):
            yield i
        for i in product(bangdan[2:-1], pinlv[0:-1], jiange, fenqv[:-4]):
            yield i
        for i in product(bangdan[-1:], pinlv[0:-1], jiange, fenqv[-3:]):
            yield i

if __name__ == '__main__':
    # crawl()
    while datetime.now().minute%10!=0:
        continue
    sleep(1)
    task.LoopingCall(crawl,True).start(600)
    # task.LoopingCall(crawl,False).start(60*60*24)
    reactor.run()
