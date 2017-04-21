# -*- coding: utf-8 -*-
import scrapy

class TrendingSpider(scrapy.Spider):
    name = "developers"
    allowed_domains = ["github.com"]
    start_urls = [
#        "https://github.com/trending",
#        "https://github.com/trending/developers"
# save target web pages to local folder is preferred in developing stage
#        "file:///home/yangfeng/cocoding/githubtrending/testpage/repositories/Trending%20repositories%20on%20GitHub%20today.html",
        "file:///home/yangfeng/cocoding/githubtrending/testpage/developers/Trending%20developers%20on%20GitHub%20today.html"
    ]

    def stripText(self, text, index):
        if text:
            if text[index]:
                return text[index].strip()
            else:
                return ""
        else:
            return ""

    def stripTimeOptionItem(self, text):
        if text:
            return text[text.find("?since="):]
        else:
            return ""

    def stripTimeOption(self, response):
        # Trending filters: today, this week, this month
        # print "time filter options"
        timeOptions = set([])
        for sel in response.xpath('//div[@class="select-menu js-menu-container js-select-menu float-right select-menu-modal-right"]/div/div/div[@class="select-menu-list"]/div/a'):
            name = sel.xpath('./span/text()').extract_first()
            link = sel.xpath('./@href').extract_first()
#            print name,link
            timeOptions.add(self.stripTimeOptionItem(link))

        return timeOptions

    def stripLanguageOption(self, response):
        # Trending filters: always shown languages
        #print "always shown language filter options"
        langOptions = set([])
        for sel in response.xpath('//ul[@class="filter-list small language-filter-list"]/li/a'):
            name = sel.xpath('./text()').extract_first()
            link = sel.xpath('./@href').extract_first()
#            print name,link
            langOptions.add(link)
            
        print "the len of language options len: "
        print len(langOptions)

        # Trending filters: other hidden languages
        #print "other hidden language filter options"
        for sel in response.xpath('//div[@class="select-menu js-menu-container js-select-menu"]/div/div/div[@class="select-menu-list"]/div/a'):
            name = sel.xpath('./span/text()').extract_first()
            link = sel.xpath('./@href').extract_first()
#            print name, link
            langOptions.add(link)
            
        print "the len of language options len: "
        print len(langOptions)

        requestUrl = response.url
        print "try to remove", requestUrl
        if requestUrl in langOptions:
            langOptions.remove(requestUrl)

        print "the len of language options len: "
        print len(langOptions)

        return langOptions

    def parse(self, response):
        # test code to save response to local file
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        # Trending filters: Repositories, Developers
        #print "content navigating filter options"
        for sel in response.xpath('//nav[@class="tabnav-tabs"]/a'):
            name = sel.xpath('./text()').extract_first()
            link = sel.xpath('./@href').extract_first()
#            print name, link
            if name.lower().strip() == "repositories":
                yield scrapy.Request(link, callback=self.parseRepo)

            if name.lower().strip() == "developers":
                yield scrapy.Request(link, callback=self.parseDeveloper)
        pass

    def parseSubRequest(self, timeOptions, langOptions, cb):
        print "parseSubRequest: ", response.url
#        timeOptions = self.stripTimeOption(response)
#        langOptions = self.stripLanguageOption(response)
        print "the len of time and language options len: "
        print len(timeOptions), len(langOptions)
        total = 0
        for sel in timeOptions:
            for lang in langOptions:
                link = lang + sel
                yield scrapy.Request(link, callback=cb)
        print "the subPage count: ", total

    def parseRepo(self, response):
        print "parseRepo", response.url
        self.parseSubRequest(self.stripTimeOption(response), self.stripLanguageOption(response), self.parseRepoItems)

    def parseRepoItems(self, response):
        print "parseRepoItems",  response.url
        # todo: how to parse gistName out in more straightward ways
        # Trending repositories items: (gistName, repoName, repoUrl, star/unstarAction description, languageIndicator, languageName, starIndicator, starCount, forkIndicator, forkCount, builderList(developerAvatar, developerName), contributorUrl, starSummary)
        #print "trending items"
        for sel in response.xpath('//ol[@class="repo-list"]/li'):
            gist = sel.xpath('.//h3/a/span/text()').extract_first()
            name = sel.xpath('.//h3/a/text()').extract()[1]
            link = sel.xpath('.//h3/a/@href').extract_first()
#            print gist[0].strip(), name[1].strip(), link[0]
#            print gist, name, link


    def parseDeveloper(self, response):
        print "parseDeveloper", response.url
#        self.parseSubRequest(response, self.parseDeveloperItems)
        self.parseSubRequest(self.stripTimeOption(response), self.stripLanguageOption(response), self.parseDeveloperItems)


    def parseDeveloperItems(self, response):
        print "parseDeveloperItems", response.url
        # todo: how to parse fullName out in more straightward ways
        # Trending developers items: (index, logo, gistName, organizationName, repoIndicator, repoDescription, repoUrl)
        #print "trending items"
        for sel in response.xpath('//ol[@class="user-leaderboard-list leaderboard-list"]/li'):
            name = sel.xpath('.//h2/a/text()').extract_first()
            fullName = sel.xpath('.//h2/a/span/text()').extract_first()
            link = sel.xpath('.//h2/a/@href').extract_first()
#            print name[0].strip(), self.stripText(fullName, 0), link[0]
#            print name, fullName, link

