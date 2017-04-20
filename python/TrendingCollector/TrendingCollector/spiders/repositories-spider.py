# -*- coding: utf-8 -*-
import scrapy

class TrendingSpider(scrapy.Spider):
    name = "repositories"
    allowed_domains = ["github.com"]
    start_urls = [
#        "https://github.com/trending",
#        "https://github.com/trending/developers"
# save target web pages to local folder is preferred in developing stage
        "file:///home/yangfeng/cocoding/githubtrending/testpage/repositories/Trending%20repositories%20on%20GitHub%20today.html",
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
        fileName = "subPageRequest.log"

        timeOptions = []
        # Trending filters: today, this week, this month
        # print "time filter options"
        for sel in response.xpath('//div[@class="select-menu js-menu-container js-select-menu float-right select-menu-modal-right"]/div/div/div[@class="select-menu-list"]/div/a'):
            name = sel.xpath('./span/text()').extract()
            link = sel.xpath('./@href').extract()
            for item in link:
                timeOptions.append(item[item.find("?since="):])
            
        # Trending filters: always shown languages
        #print "always shown language filter options"
        languageOptions = []
        for sel in response.xpath('//ul[@class="filter-list small language-filter-list"]/li/a'):
            name = sel.xpath('./text()').extract()
            link = sel.xpath('./@href').extract()
            for item in link:
                for lang in timeOptions:
                    languageOptions.append(item + lang)
            
        # todo: how to avoid the duplicate sub page request?
        # nextPage = languageOptions[i] + timeOptions[j]
        # yield scrapy.Request(nextPage, callback=self.parse)
        # Trending filters: other hidden languages
        #print "other hidden language filter options"
        for sel in response.xpath('//div[@class="select-menu js-menu-container js-select-menu"]/div/div/div[@class="select-menu-list"]/div/a'):
            name = sel.xpath('./span/text()').extract()
            link = sel.xpath('./@href').extract()
            for item in link:
                for lang in timeOptions:
                    nextPage = item + lang
                    languageOptions.append(nextPage)
                    yield scrapy.Request(nextPage, callback=self.parse)
            
        print response.url
        with open(fileName, 'ab') as file:
            file.write(response.url + "\n")

#        print(languageOptions)
#        print(timeOptions)

        # todo: how to parse gistName out in more straightward ways
        # Trending repositories items: (gistName, repoName, repoUrl, star/unstarAction description, languageIndicator, languageName, starIndicator, starCount, forkIndicator, forkCount, builderList(developerAvatar, developerName), contributorUrl, starSummary)
        #print "trending items"
        for sel in response.xpath('//ol[@class="repo-list"]/li'):
            gist = sel.xpath('.//h3/a/span/text()').extract()
            name = sel.xpath('.//h3/a/text()').extract()
            link = sel.xpath('.//h3/a/@href').extract()
            #print gist[0].strip(), name[1].strip(), link[0]

        pass
