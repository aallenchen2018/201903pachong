# -*- coding: utf-8 -*-
import scrapy
import re
import json
from JD.items import BraItem




class BraSpider(scrapy.Spider):
    name = 'bra'
    # allowed_domains = ['search.jd.com/Search?keyword=bra']
    start_urls = ['https://search.jd.com/search?keyword=%E5%86%85%E8%A1%A3%E5%A5%B3&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.V00--&wq=%E5%86%85%E8%A1%A3&cid3=1364']

    def parse(self, response):
        results=list(set(response.css('#J_goodsList > ul > li.gl-item::attr(data-sku)').extract()))
        for productID in results:
            print('+++++',productID)
            url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv5427&productId='+productID+'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=url,callback=self.parse_page,meta={'productID':productID})

    def parse_page(self,response):
        productID=response.meta['productID']
        page=int(re.search(r'maxPage.*?:(\d+),',response.text,re.S).group(1))
        for pn in range(0,page):
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv5427&productId='+productID+'&score=0&sortType=5&page='+str(pn)+'&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=url,callback=self.parse_item,dont_filter=True)

    def parse_item(self,response):
        results=response.text.replace('fetchJSON_comment98vv5427(','').replace(');','')
        results = json.loads(results)
        for comment in results['comments']:
            item = BraItem()
            item['content']=comment['content']
            item['id'] = comment['id']
            item['productColor'] = comment['productColor']
            item['productSize'] = comment['productSize']
            item['referenceName'] = comment['referenceName']
            item['score'] = comment['score']
            yield item
