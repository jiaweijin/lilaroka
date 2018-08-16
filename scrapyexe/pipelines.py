# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# ''utf_8_sig' ----解决编码问题
import re

import csv

import codecs

import itertools

import os

class ScrapyexePipeline(object):
    def process_item(self, item, spider):
        #用itemloader的时候再用：
        # title = item['title']
        # url = item['url']
        # author = item['author']
        # group = item['group']
        # content = item['content']
        #
        # item['content'] = re.findall(r'(?<=\\x01)(.+?)(?=\\)',content)#提取出所有中文文本
        # item['title'] = title.replace('\n','')
        # item['author'] = author.strip()
        return item

class DianpingContentPipeline(object):
    def process_item(self,item,spider):

        with codecs.open('dianpingcontent.txt','a','utf_8_sig') as output:
            if item['content']:
                output.write('标题：'+item['title'] + '\n'
                             '作者：'+item['author'] + '\n'
                             '小组：' + item['group'] +'\n'
                             '内容：'+item['content']+'\n\n')
            else:
                output.write('标题：' + item['title'] + '\n'
                             '作者：' + item['author'] + '\n'
                             '小组：' + item['group'] + '\n\n')
        return item