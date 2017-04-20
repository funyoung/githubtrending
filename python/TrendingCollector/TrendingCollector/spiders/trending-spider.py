# -*- coding: utf-8 -*-
import scrapy

class TrendingSpider(scrapy.Spider):
    name = "trending"
    allowed_domains = ["github.com"]
    start_urls = [
        "https://github.com/trending",
        "https://github.com/trending/developers"
# save target web pages to local folder is preferred in developing stage
#        "file:///home/yangfeng/cocoding/githubtrending/testpage/repositories/Trending%20repositories%20on%20GitHub%20today.html",
#        "file:///home/yangfeng/cocoding/githubtrending/testpage/developers/Trending%20developers%20on%20GitHub%20today.html"
    ]

    def stripText(self, text, index):
        if text:
            if text[index]:
                return text[index].strip()
            else:
                return ""
        else:
            return ""

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
            print name, link
            
        # todo: how to parse gistName out in more straightward ways
        # Trending repositories items: (gistName, repoName, repoUrl, star/unstarAction description, languageIndicator, languageName, starIndicator, starCount, forkIndicator, forkCount, builderList(developerAvatar, developerName), contributorUrl, starSummary)
        #print "trending items"
        for sel in response.xpath('//ol[@class="repo-list"]/li'):
            gist = sel.xpath('.//h3/a/span/text()').extract()
            name = sel.xpath('.//h3/a/text()').extract()
            link = sel.xpath('.//h3/a/@href').extract()
            print gist[0].strip(), name[1].strip(), link[0]

        # todo: how to parse fullName out in more straightward ways
        # Trending developers items: (index, logo, gistName, organizationName, repoIndicator, repoDescription, repoUrl)
        #print "trending items"
        for sel in response.xpath('//ol[@class="user-leaderboard-list leaderboard-list"]/li'):
#name = sel.xpath('.//h2/a/text()').extract()
            name = sel.xpath('.//h2/a/text()').extract()
            fullName = sel.xpath('.//h2/a/span/text()').extract()
            link = sel.xpath('.//h2/a/@href').extract()
            print name[0].strip(), self.stripText(fullName, 0), link[0]

        pass
