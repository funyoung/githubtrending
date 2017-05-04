# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import scrapy
import re

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

    def stripTimeOption(self, bs):
        # Trending filters: today, this week, this month
        # print "time filter options"
        timeOptions = set([])
#        for sel in response.xpath('//div[@class="select-menu js-menu-container js-select-menu float-right select-menu-modal-right"]/div/div/div[@class="select-menu-list"]/div/a'):
#            name = sel.xpath('./span/text()').extract_first()
#            link = sel.xpath('./@href').extract_first()
        for l in bs.find(self.time_menu_list, role="menu").find_all('a'):
            link = l.get('href')
            name = l.find('span').string
            print link, name
            timeOptions.add(self.stripTimeOptionItem(link))
            
        print "the len of time options len: "
        print len(timeOptions)

        return timeOptions

    def stripLanguageOption(self, bs, requestUrl):
        # Trending filters: always shown languages
        #print "always shown language filter options"
        langOptions = set([])
#        for sel in response.xpath('//ul[@class="filter-list small language-filter-list"]/li/a'):
#            name = sel.xpath('./text()').extract_first()
#            link = sel.xpath('./@href').extract_first()
        for l in bs.find('ul', class_="filter-list small language-filter-list").find_all('a'):
            link = l.get('href')
            name = l.string
            print link, name
            langOptions.add(link)
            
        print "the len of language options len: "
        print len(langOptions)
            
        # Trending filters: other hidden languages
        #print "other hidden language filter options"
#        for sel in response.xpath('//div[@class="select-menu js-menu-container js-select-menu"]/div/div/div[@class="select-menu-list"]/div/a'):
#            name = sel.xpath('./span/text()').extract_first()
#            link = sel.xpath('./@href').extract_first()
        for l in bs.find(self.language_menu_list, role="menu").find_all('a'):
            link = l.get('href')
            name = l.find('span').string
            print link, name
            langOptions.add(link)
            
        print "the len of language options len: "
        print len(langOptions)

        print "try to remove", requestUrl
        if requestUrl in langOptions:
            langOptions.remove(requestUrl)

        print "the len of language options len: "
        print len(langOptions)

        return langOptions

    def has_class(self, tag):
        return tag.has_attr('class')

    def has_data_pjax(self, tag):
        return tag.has_attr('data-pjax')

    def time_menu_list(self, tag):
        return self.has_class(tag) and not self.has_data_pjax(tag)

    def language_menu_list(self, tag):
        return self.has_class(tag) and self.has_data_pjax(tag)

    def small_language_list(self, tag):
        return self.has_class(tag) and self.has_data_pjax(tag)

    def parse(self, response):
        # test code to save response to local file
#        filename = response.url.split("/")[-2] + '.html'
#        with open(filename, 'wb') as f:
#            f.write(response.body)
#        self.log('Saved file %s' % filename)
        fileName = "subPageRequest.log"
        with open(fileName, 'wb') as file:
            file.write(response.url + "\n")

        bs = BeautifulSoup(response.body)
        timeOptions = self.stripTimeOption(bs);
        langOptions = self.stripLanguageOption(bs, response.url);
#        requestUrl = response.url

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

#        b = BeautifulSoup('<a href="/zeit/pkg"> <span class="text-normal">zeit / </span>pkg </a>')
#        a = b.find('a')
#        print a.get('href')
#        print a.find('span').string
#        print a.string
#        print a.get_text()
#        print a.contents[2]
#        print a.contents[1]
#        print a.contents[0]
#        print len(a.contents)
#
#        print b.find_all('a')
#        i = b.find('a')
##        for i in b.find_all('a'):
#        print i
#        text = i.get_text()
#        print text
#        text2 = text.split('/')
#        print text2

        pass

    def lastContent(self, tag):
        index = len(tag.contents) - 1
        return tag.contents[index]
    
    def parseRepoItems(self, response):
        bs = BeautifulSoup(response.body)
        for sel in bs.find('ol', class_="repo-list").find_all('li'):
           a = sel.find('h3').find('a')
           link = a.get('href')
           name = a.contents[2].strip()
           gist = a.find('span').string
           print link, gist, name

           p = sel.find('p')
#           print len(p.contents)
           index = len(p.contents) - 1
           descText = p.contents[index].strip()
           descIcon = p.find('g-emoji')
           if descIcon is None:
               descIcon = ""
           else:
               descIcon = descIcon.get("fallback-src")
#           print descText, " <", descIcon, ">"
            
           langColor = sel.find('span', class_="repo-language-color ml-0")
           if langColor is None:
               langColor = ""
           else:
               langColor = langColor.get("style")
           lang = sel.find('span', itemprop="programmingLanguage")
           if lang is None:
               lang = ""
           else:
               lang = lang.string.strip()
#           print lang, " < ", langColor

           # stargazers and network
           starFork = sel.find_all('a', class_="muted-link mr-3")
           starLink = starFork[0].get('href')
           forkLink = starFork[1].get('href')
           starLabel = self.lastContent(starFork[0]).strip()
           forkLabel = self.lastContent(starFork[1]).strip()
           print starLabel, forkLabel, starLink, forkLink
           
           # Built by
           contributors = []
           c = sel.find('a', class_="no-underline")
           action = c.get('href')
           for i in c.find_all('img'):
               title = i.get('title')
               src = i.get('src')
               print src
               contributors.append(title)
#               contributors.append(src)
           print action, len(contributors), contributors
           
           # summary star
           starSum = sel.find('span', class_="float-right")
           starSum = self.lastContent(starSum).strip()
           print starSum

    def parseRepoItemsWithoutBs(self, response):
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

