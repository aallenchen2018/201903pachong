# -*- coding: utf-8 -*-
import scrapy
from spider05.items import Spider05Item
import time
import re
import json





# inputpn=int(input('输入页码：     '))
class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    # allowed_domains = ['sz.lianjia.com/zufang']
    start_urls = ['https://sz.lianjia.com/zufang/pg2/#contentList']
  
    def parse(self, response):
        quotes=response.css('.content__list--item--main')
        
        for quote in quotes:
            item=Spider05Item()
            item['name']=quote.css('.content__list--item--title.twoline a::text').extract_first().strip()
            item['price']=quote.css('.content__list--item-price em::text').extract_first()
            item['time']=quote.css('.content__list--item--time::text').extract_first()
            yield item
            
            
            # next_page=response.css('#content > div.content__article > div.content__pg > a.next::text').extract_first()
            #content > div.content__article > div.content__pg > a.next
            # response=response.replace('define("util/env", [], function() ','').replace(');','')
            # dict=json.loads(response)

            # next_page=response.json.loads('e && e.length) ').extract_first() 
            
            #content > div.content__article > div.content__pg > a.next
            #content > div.content__article > div.content__pg > a.next

 




        for i in range(3,99):
            
            url='https://sz.lianjia.com/zufang/pg'+str(i)+'/#contentList'
            
            
            yield scrapy.Request(url=url,callback=self.parse)
            




       



