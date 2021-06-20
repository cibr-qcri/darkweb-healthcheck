import os
import re

from bs4 import BeautifulSoup
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy_redis.spiders import RedisSpider
from twisted.internet.error import DNSLookupError

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
        self.site_info = {}
        self.seq_number = 0
        self.dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.domain_count = dict()

    def parse(self, response):
        url = self.helper.unify(response.url)

        soup = BeautifulSoup(response.text, "lxml")

        if ONION_PAT.match(response.url) and 'Onion.ws is a darknet gateway or proxy' not in soup.text:
            domain = self.helper.get_domain(url)

            item = TorspiderItem()
            item['url'] = url
            item['domain'] = domain

            yield item

    def handle_error(self, failure):
        self.logger.debug(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
