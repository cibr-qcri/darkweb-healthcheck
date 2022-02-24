import re

from scrapy_redis.spiders import RedisSpider

from ..items import TorspiderItem
from ..support import TorHelper

ONION_PAT = re.compile(r"(?:https?://)?(([^/.]*)\.)*(\w{56}|\w{16})\.onion")


class TorSpider(RedisSpider):
    name = "darkweb-healthcheck"
    start_source = {}
    log_timeval = 3600
    tor_ref_timeval = 600
    seq_number = 0

    def __init__(self):
        RedisSpider.__init__(self)
        self.helper = TorHelper()

    def parse(self, response):
        url = self.helper.unify(response.url)

        if ONION_PAT.match(response.url):
            domain = self.helper.get_domain(url)
            item = TorspiderItem()
            item['url'] = url
            item['is_online'] = True
            item['domain'] = domain
            item['version'] = 'v3' if len(domain.replace('.onion', '')) > 16 else 'v2',
            if not response.staus or response.status > 210:
                item['is_online'] = False

            yield item
