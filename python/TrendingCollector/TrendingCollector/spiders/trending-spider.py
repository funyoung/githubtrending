# -*- coding: utf-8 -*-
import scrapy

class TrendingSpider(scrapy.Spider):
    name = "trending"
    allowed_domains = ["github.com"]
    start_urls = [
#        "https://github.com/trending",
#        "https://github.com/trending/developers"
# save target web pages to local folder is preferred in developing stage
        "file:///home/yangfeng/cocoding/githubtrending/testpage/repositories/Trending%20repositories%20on%20GitHub%20today.html",
#        "file:///home/yangfeng/cocoding/githubtrending/testpage/developers/Trending%20developers%20on%20GitHub%20today.html"
    ]

    def stripTextArray(self, textArray, index):
        if len(textArray) > index:
            return textArray[index].strip()
        else:
            return ""

    def stripText(self, text):
        if text:
            return text.strip()
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
#        filename = response.url.split("/")[-2] + '.html'
#        with open(filename, 'wb') as f:
#            f.write(response.body)
#        self.log('Saved file %s' % filename)
        fileName = "subPageRequest.log"
        with open(fileName, 'wb') as file:
            file.write(response.url + "\n")

        timeOptions = self.stripTimeOption(response);
        langOptions = self.stripLanguageOption(response);

        isDeveloper = 0
        for lang in langOptions:
            if "/developers" in lang:
                isDeveloper = 1
            break

        for lang in langOptions:
            for time in timeOptions:
                if isDeveloper == 1:
                    link = lang.replace("/developers", "")
#                    yield scrapy.Request(link + time, callback=self.parseRepoItems)
#                    yield scrapy.Request(lang + time, callback=self.parseDeveloperItems)
                else:
#                    yield scrapy.Request(lang + time, callback=self.parseRepoItems)
                    link = lang.replace("/trending", "/trending/developers")
#                    yield scrapy.Request(link + time, callback=self.parseDeveloperItems)

        self.parseRepoItems(response)
        self.parseDeveloperItems(response)

        pass

    def parseRepoItems(self, response):
        print "parseRepoItems",  response.url
        fileName = "subPageRequest.log"
        with open(fileName, 'ab') as file:
            file.write(response.url + "\n")
            
        # todo: how to parse gistName out in more straightward ways
        # Trending repositories items: (gistName, repoName, repoUrl, star/unstarAction description, languageIndicator, languageName, starIndicator, starCount, forkIndicator, forkCount, builderList(developerAvatar, developerName), contributorUrl, starSummary)
        #print "trending items"
        for sel in response.xpath('//ol[@class="repo-list"]/li'):
            gist = sel.xpath('.//h3/a/span/text()').extract_first()
            name = self.stripText(sel.xpath('.//h3/a/text()')[1].extract())
            link = "https://github.com" + sel.xpath('.//h3/a/@href').extract_first()
#            print gist[0].strip(), name[1].strip(), link[0]
#            print gist, name, link
#            skip right-top star/unstar action
#            descIcon = sel.xpath('.//div[@class="py-1"]/p/g-emoji/@fallback-src').extract()
            descIcon = self.stripTextArray(sel.xpath('.//div[@class="py-1"]/p/g-emoji/@fallback-src').extract(), 0)
            descArray = sel.xpath('.//div[@class="py-1"]/p/text()').extract()
            desc = self.stripTextArray(descArray, 0)
            if descIcon != "":
                desc = self.stripTextArray(descArray, 1)
#            print desc, "<", descIcon, ">" #, descArray

            # repo extra info
            extra = sel.xpath('.//div[@class="f6 text-gray mt-2"]')
            # programmingLanguage
            langColor = self.stripTextArray(extra.xpath('./span[@class="repo-language-color ml-0"]/@style').extract(), 0)
            lang = self.stripTextArray(extra.xpath('./span[@itemprop="programmingLanguage"]/text()').extract(), 0)
            print lang, "<", langColor, ">" #, descArray

            # stargazers and network
            starFork = extra.xpath('./a[@class="muted-link mr-3"]').extract()
            print len(starFork), starFork

            # Built by
            builtBy = extra.xpath('./a[@class="no-underline"]').extract()
            print builtBy

            # summary star
            summaryStar = extra.xpath('./span/text()').extract()
            print summaryStar

    def parseDeveloperItems(self, response):
        print "parseDeveloperItems", response.url
        fileName = "subPageRequest.log"
        with open(fileName, 'ab') as file:
            file.write(response.url + "\n")

        # todo: how to parse fullName out in more straightward ways
        # Trending developers items: (index, logo, gistName, organizationName, repoIndicator, repoDescription, repoUrl)
        #print "trending items"
        for sel in response.xpath('//ol[@class="user-leaderboard-list leaderboard-list"]/li'):
            name = self.stripText(sel.xpath('.//h2/a/text()').extract_first())
            fullName = self.stripText(sel.xpath('.//h2/a/span/text()').extract_first())
            link = sel.xpath('.//h2/a/@href').extract_first()
#            print name[0].strip(), self.stripText(fullName, 0), link[0]
            print name, fullName, link

