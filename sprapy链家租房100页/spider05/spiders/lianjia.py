# -*- coding: utf-8 -*-
import scrapy
from spider05.items import Spider05Item
import time
import re
import json

#注意事项：
##记得在settings.py 关闭robert
###定位网页元素时，如果elements找不到，就在network找  
####保存到-o json时候，在settings.py里面加上 ---FEED_EXPORT_ENCODING = 'utf-8'

class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    start_urls = ['https://sz.lianjia.com/zufang/#contentList']    #第一页为初始页
  
    def parse(self, response):
        quotes=response.css('.content__list--item--main')
        
        for quote in quotes:
            item=Spider05Item()
            item['name']=quote.css('.content__list--item--title.twoline a::text').extract_first().strip()
            item['price']=quote.css('.content__list--item-price em::text').extract_first()
            item['time']=quote.css('.content__list--item--time::text').extract_first()
            yield item
            
            #链家的 next page元素找不到下一页的数字，所以不能采集；这里用for 循环翻页

        for i in range(2,100):
            
            url='https://sz.lianjia.com/zufang/pg'+str(i)+'/#contentList'
            
            yield scrapy.Request(url=url,callback=self.parse)
            




       



