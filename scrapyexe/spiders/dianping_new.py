# -*- coding: utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapyexe.items import ScrapyexeItem
from scrapy.loader import ItemLoader
from scrapy import Request
import re
import json
class ScrapyexeSpider(Spider):
    name = 'dianping'
    allowed_domains = ['www.dianping.com']
    # custom_settings = {
    #     'referer':'http://s.dianping.com/chengdu/group?utm_source=dp_pc_index',
    #     'cookie':'cye=chengdu; cy=8',
    #     'X-Requested-With':'XMLHttpRequest'
    # }

    def start_requests(self):
        for i in range(1,400):
            if i == 1:
                base_url = 'http://s.dianping.com/chengdu/group?utm_source=dp_pc_index'
                #print('首页')
                yield Request(base_url,callback=self.parse) #第一页是首页
            else:
                url = 'http://s.dianping.com/ajax/queryRecommendNote?cityId=8&page={i}&limit=40'.format(i = i)
                #print('页数：',i)
                yield Request(url,callback=self.parse_page_add,headers={'referer':'http://s.dianping.com/chengdu/group?utm_source=dp_pc_index',
         'cookie':'cye=chengdu; cy=8'})

    def parse(self,response):
        #print('相应头：',response.headers)
        #print('响应内容：',response.text)
        for r in response.xpath('//*[@id="list-recomend"]/ul/li'):
            item = ScrapyexeItem()
            item['title'] = r.xpath('string(./div/h3/a/text())').extract_first().strip() #返回是list
            item['url'] = r.xpath('string(./div/h3/a/@href)').extract_first().strip()
            item['author'] = r.xpath('string(./div/div/a[2]/text())').extract_first().strip()
            item['group'] = r.xpath('string(./div/div/a[3]/text())').extract_first().strip()
            url = str(item['url'])
            content = ''
            yield Request(url,meta={'content': content,'item':item},callback=self.parse_details,dont_filter=True)
            #break
#http://s.dianping.com/topic/39465388?utm_source=forum_pc_index
    def parse_page_add(self,response):
        js = json.loads(response.body)
        list = js['notes']
        for post in list:
            item = ScrapyexeItem()
            item['title'] = post['noteTitle']
            noteId = post['noteId']
            item['url'] = 'http://s.dianping.com/topic/'+str(noteId) +'?utm_source=forum_pc_index'
            item['author'] = post['userInfo']['userNickName']
            item['group'] = post['groupName']
            url = str(item['url'])
            content = ''
            yield Request(url,meta={'content': content,'item':item},callback=self.parse_details,dont_filter=True)
            #break
    def parse_details(self, response):
        details_info = response.xpath('/html/body/div[2]/div[3]/div[2]')
        item_content = ScrapyexeItem()
        content = response.meta['content']
        item = response.meta['item']
        if details_info:
            content_num = len(response.selector.xpath('/html/body/div[2]/div[3]/div[2]/div[3]/div[*]').extract())
            print(content_num)
            for i in range(content_num):
                content += response.selector.xpath('/html/body/div[2]/div[3]/div[2]/div[3]/div[%d+1]'%(i)).extract_first()
                # print(content)
            zh = re.compile(u'[\u4e00-\u9fa5]+') #提取中文的正则
            content = re.findall(zh,content)
            content = ''.join(content).replace('微软雅黑','').replace('宋体','')
            #print(content)
        item_content['title'] = item['title']
        item_content['url'] = item['url']
        item_content['author'] = item['author']
        item_content['group'] = item['group']
        item_content['content'] = content
        yield item_content

