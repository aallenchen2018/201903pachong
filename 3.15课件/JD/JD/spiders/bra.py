# -*- coding: utf-8 -*-
import scrapy
import re
import json
from JD.items import BraItem

#分析网页的主要思路
    #（1）我们主要是为了获取商品的销售数据（评论数据），首先找到商品的销售数据，跟网页呈现的相同
    #（2）找到对应的链接，分析链接里面包含的主要信息：有商品的ID——ProductId、评论数据的页码——page
    #（3）接下来主要考虑不同的商品对应的ID，看网站的URL会发现有ProductID的信息，就可以以此确定通过京东搜索页面，
    #     输入关键字，我们可以基于呈现的页面来分析，可以获取商品的ProductID

#爬虫的主要思路：
    #（1）通过搜索商品关键字，来得到关于商品的页面，点击“销量”进行排序，基于该页面的URL完成，发送请求，获取商品ProductID
    #（2）得到商品ProductID之后，构建评论数据对应的链接，进行请求，获得该商品的评论数据最大页码maxpage
    #（3）得到最大页码之后，可以重新基于商品ProductId和页数page，重新构建评论数据的URL，进行请求，获得每个商品，每页下面的销售数据
    #（4）获得响应进行解析，提取感兴趣的数据，并进行保存。


class BraSpider(scrapy.Spider):
    name = 'bra'
    # allowed_domains = ['search.jd.com/Search?keyword=bra']
    start_urls = ['https://search.jd.com/search?keyword=%E5%86%85%E8%A1%A3%E5%A5%B3&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.V00--&wq=%E5%86%85%E8%A1%A3&cid3=1364']

    def parse(self, response):
        '''
        解析响应，获取产品ID,确定下一步请求
        :param response:
        :return:
        '''
        #提取产品ID,并进行去重
        results=list(set(response.css('#J_goodsList > ul > li.gl-item::attr(data-sku)').extract()))
        for productID in results:
            #下一步请求，主要是为了获取每个产品的评论页码数
            url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv5427&productId='+productID+'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=url,callback=self.parse_page,meta={'productID':productID})
        
        



    def parse_page(self,response):
        '''
        提取产品的评论页码数，并确定下一步请求
        :param response:
        :return:
        '''
        productID=response.meta['productID']#获得产品ID
        page=int(re.search(r'maxPage.*?:(\d+),',response.text,re.S).group(1))#提取页码数

        results = response.text.replace('fetchJSON_comment98vv5427(', '').replace(');', '')
        results = json.loads(results)
        for comment in results['comments']:
            yield self.get_item(comment)

        for pn in range(1,page):#翻页
            #下一步的请求，主要是为了获取每一步的评论数
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv5427&productId='+productID+'&score=0&sortType=5&page='+str(pn)+'&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=url,callback=self.parse_item)

    def parse_item(self,response):
        '''
        提取评论数
        :param response:
        :return:
        '''
        #将响应体改造成类似json的字符串
        results=response.text.replace('fetchJSON_comment98vv5427(','').replace(');','')
        results = json.loads(results)
        for comment in results['comments']:
            yield self.get_item(comment)

    def get_item(self,comment):
        item = BraItem()
        item['content'] = comment['content']
        item['id'] = comment['id']
        item['productColor'] = comment['productColor']
        item['productSize'] = comment['productSize']
        item['referenceName'] = comment['referenceName']
        item['score'] = comment['score']
        return item