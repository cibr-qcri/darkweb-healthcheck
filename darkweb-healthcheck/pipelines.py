import os
from datetime import datetime
from hashlib import sha256

from scrapy_redis.pipelines import RedisPipeline

from .es7 import ES7
from .support import TorHelper


class TorspiderPipeline(RedisPipeline):

    def __init__(self, server):
        super().__init__(server)
        self.dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.helper = TorHelper()
        self.date = datetime.today()
        self.es = ES7()

    def process_item(self, item, spider):
        url = item["url"]
        domain = item['domain']

        timestamp = int(datetime.now().timestamp() * 1000)
        es_id = domain + str(timestamp)

        es_id = sha256(es_id.encode("utf-8")).hexdigest()

        tag = {
            "timestamp": timestamp,
            "type": "darkweb-healthcheck",
            "domain": domain,
            "url": url
        }

        self.es.persist_report(tag, es_id)
