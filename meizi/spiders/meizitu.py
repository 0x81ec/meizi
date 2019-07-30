# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from urllib import request

import os.path

class MeizituSpider(CrawlSpider):
    name = 'meizitu'

    allowed_domains = ['www.netbian.com']

    start_urls = ['http://www.netbian.com']

    rules = (
        # http://www.netbian.com/index_6.htm
        Rule(LinkExtractor(allow=r'.*/index_[\d]*\.htm'), callback='parse_item', follow=True),
            
        Rule(LinkExtractor(allow=r'.*/desk/[\d]*\.htm'), callback='parse_meizi', follow=True),
    )
    def parse_item(self, response):

        base_url = "http://www.netbian.com"

        meizi = response.xpath("//li/a/@href").getall()

        for m in meizi:

            scrapy.Request(base_url+m)

            print(base_url+m)
    
    def parse_meizi(self, response):

       base_path="G:/bian/"

       tp = response.xpath("//div[@class='action']/a[last()-1]/text()").get()

       meizi = response.xpath("//div[@class='pic']/p/a/img/@src").get()

       path = base_path+tp

       if not os.path.exists(path):
           os.makedirs(path)

       request.urlretrieve(meizi,path+"/"+meizi.split("/")[-1])

       print(meizi+"---"*10+"ok")
