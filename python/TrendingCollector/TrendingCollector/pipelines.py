# -*- coding: utf-8 -*-
# SEETO:
# http://www.cnblogs.com/rwxwsblog/p/4572367.html
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

from TrendingCollector.translate.youdaotranslate import *

class plainTextWithEncodingCnblogsPipeline(object):
    translator = youdao_API('1749671432')

    def __init__(self):
        self.file = codecs.open('trending.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
#        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        d = dict(item)
        descText = d['desc']
        self.translator.get_url(descText)
        jsonText =  json.loads(self.translator.get_json(descText))
        target = jsonText.get('translation')
#        print target
        line = ""
        line = line + d['title'] + "\n"
        line = line + d['link'] + "\n"
        line = line + descText + "\n"
        line = line + target[0] + "\n"
        line = line + "\n"

        self.file.write(line)
        
        return item
    def spider_closed(self, spider):
        self.file.close()


class JsonWithEncodingCnblogsPipeline(object):
    def __init__(self):
        self.file = codecs.open('trending.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()

class MySQLStoreCnblogsPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
    
    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    #pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d
    #将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
        linkmd5id = self._get_linkmd5id(item)
        #print linkmd5id
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from cnblogsinfo where linkmd5id = %s
        """, (linkmd5id, ))
        ret = conn.fetchone()

        if ret:
            conn.execute("""
                update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
            """, (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id))
            #print """
            #    update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
            #""", (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id)
        else:
            conn.execute("""
                insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated) 
                values(%s, %s, %s, %s, %s, %s)
            """, (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now))
            #print """
            #    insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated)
            #    values(%s, %s, %s, %s, %s, %s)
            #""", (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now)
    #获取url的md5编码
    def _get_linkmd5id(self, item):
        #url进行md5处理，为避免重复采集设计
        return md5(item['link']).hexdigest()
    #异常处理
    def _handle_error(self, failue, item, spider):
        log.err(failure)

#class TrendingcollectorPipeline(object):
#    def process_item(self, item, spider):
#        return item
