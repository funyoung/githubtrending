# -*- coding: utf-8 -*-
import scrapy


class TrendingSpider(scrapy.Spider):
    name = "trending"
    allowed_domains = ["github.com"]
    start_urls = [
        "https://github.com/trending"
    ]

    def parse(self, response):
        print response
        pass
