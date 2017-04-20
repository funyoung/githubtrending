# -*- coding: utf-8 -*-
import scrapy


class TrendingSpider(scrapy.Spider):
    name = "trending"
    allowed_domains = ["github.com"]
    start_urls = [
        "https://github.com/trending"
    ]

    def parse(self, response):
        # Trending filters: Repositories, Developers
        #print "content navigating filter options"
        for sel in response.xpath('//nav[@class="tabnav-tabs"]/a'):
            name = sel.xpath('./text()').extract()
            link = sel.xpath('./@href').extract()
            print name, link

        # Trending filters: today, this week, this month
        # print "time filter options"
        for sel in response.xpath('//div[@class="select-menu js-menu-container js-select-menu float-right select-menu-modal-right"]/div/div/div[@class="select-menu-list"]/div/a'):
            name = sel.xpath('./span/text()').extract()
            link = sel.xpath('./@href').extract()
            print name,link
            
        # Trending filters: always shown languages
        #print "always shown language filter options"
        for sel in response.xpath('//ul[@class="filter-list small language-filter-list"]/li/a'):
            name = sel.xpath('./text()').extract()
            link = sel.xpath('./@href').extract()
            print name,link
            
        # Trending filters: other hidden languages
        #print "other hidden language filter options"
        for sel in response.xpath('//div[@class="select-menu js-menu-container js-select-menu"]/div/div/div[@class="select-menu-list"]/div/a'):
            name = sel.xpath('./span/text()').extract()
            link = sel.xpath('./@href').extract()
            print name,link
            
        pass
