# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TorspiderItem(scrapy.Item):
    url = scrapy.Field()
    domain = scrapy.Field()
    version = scrapy.Field()
    is_online = scrapy.Field()
