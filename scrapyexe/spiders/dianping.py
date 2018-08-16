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
class ScrapyexeSpider(Spider):
    name = 'dianping_old'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://s.dianping.com/chengdu/group?utm_source=dp_pc_index']

    def parse(self,response):
        item_num = len(response.selector.xpath('//*[@id="list-recomend"]/ul/li[*]/div/h3').extract())
        print(item_num)
        for i in range(item_num):
            item = ScrapyexeItem()
            item['title'] = response.selector.xpath('//*[@id="list-recomend"]/ul/li[%d+1]/div/h3/a/text()'%(i)).extract()[0] #返回是list
            item['url'] = response.selector.xpath('//*[@id="list-recomend"]/ul/li[%d+1]/div/h3/a/@href'%(i)).extract()[0]
            author = response.selector.xpath('//*[@id="list-recomend"]/ul/li[%d+1]/div/div/a[2]/text()'%(i)).extract()[0]
            item['author'] = author.strip()
            item['group']=response.selector.xpath('//*[@id="list-recomend"]/ul/li[%d+1]/div/div/a[3]/text()'%(i)).extract()[0]
            url = str(item['url'])
            #print(url)
            # url = 'https://www.jianshu.com'+url
            # yield Request(url, callback=self.parse_detail)
            yield item
            yield Request(url, callback=self.parse_details, dont_filter=True)
            break
    def parse_details(self, response):
        details_info = response.xpath('/html/body/div[2]/div[3]/div[2]')
        if details_info:
            # l = ItemLoader(ScrapyexeItem(),details_info)
            # l.add_xpath('content','/html/body/div[2]/div[3]/div[2]/div[3]/text()')
            # yield l.load_item()
            item_content = ScrapyexeItem()
            content_num = len(response.selector.xpath('/html/body/div[2]/div[3]/div[2]/div[3]/div[*]').extract())

            print(content_num)
            content = ''
            for i in range(content_num):
                content += response.selector.xpath('/html/body/div[2]/div[3]/div[2]/div[3]/div[%d+1]'%(i)).extract()[0]
                # print(content)
            zh = re.compile(u'[\u4e00-\u9fa5]+') #提取中文的正则
            content = re.findall(zh,content)
            content = ''.join(content)
            #print(content)
            item_content['content'] = content
            yield item_content

