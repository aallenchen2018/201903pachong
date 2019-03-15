# -*- coding: utf-8 -*-
import scrapy
from spider03.items import QuoteItem

##记得在settings 关闭robert
###如果elements找不到，就在network找  定位
####保存到-o json时候，在setting.py里面加上 ---FEED_EXPORT_ENCODING = 'utf-8'

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes=response.css('.quote')
        for quote in quotes:       
            item=QuoteItem()
            item['text']=quote.css('.text::text').extract_first()
            item['author']=quote.css('.author::text').extract_first()
            item['tags']=quote.css('.tags .tag::text').extract()
            yield item
# next_page=response.css('.pager .next a::attr(href)').extract_first()  ##如果用extract()就返回列表
            next_page=response.css('.col-md-8  .pager .next a::attr(href)').extract_first() 
            # body > div > div:nth-child(2) > div.col-md-8 > nav > ul > li.next > a
########用>号一定时下级紧跟上级，3级内定义完。   
       
       
        
        print(next_page)
        url=response.urljoin(next_page)
        yield scrapy.Request(url=url,callback=self.parse)
  
       

