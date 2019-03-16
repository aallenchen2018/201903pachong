# -*- coding: utf-8 -*-
import scrapy
from dangdang.items import DangdangItem

#找productID的时候 sku这个属性就是取不出来，后来用a标签的ID代替



class JiqixuexiSpider(scrapy.Spider):
    name = 'jiqixuexi'
    # allowed_domains = ['http://www.dangdang.com']
    start_urls = ['http://search.dangdang.com/?key=%BB%FA%C6%F7%D1%A7%CF%B0&act=input']

    def parse(self, response):
        results=list(set(response.css('#component_59 li::attr(id)').extract()))
        # print(results)
        for productID in results:
            productID=productID[1:]
            url='http://product.dangdang.com/index.php?r=comment%2Flist&productId='+productID+'&categoryPath=01.54.92.02.00.00&mainProductId='+productID+'&mediumId=0&pageIndex=2&sortType=1&filterType=1&isSystem=1&tagId=0&tagFilterCount=0&template=publish&long_or_short=short'
        
            # print(url)
            yield scrapy.Request(url=url,callback=self.parse_page,meta={'productID':productID})

    def parse_page(self,response):
        productID=response.meta['productID']
      
        page=3
     
        results=response.css('div.con.shoplist')
  
        for result in results:
            item=DangdangItem()
            item['comment']=result.css('div.describe_detail > span > a::text').extract_first()
            print(item['comment'])
            
            item['status']=result.css('div.items_right > div.starline.clearfix::text').extract_first()
            yield item
           

        # for pn in range(1,page):
        #     url='http://product.dangdang.com/index.php?r=comment%2Flist&productId=22631853&categoryPath=01.03.51.00.00.00&mainProductId='+productID+'&mediumId=0&pageIndex='+str(pn)+'&sortType=1&filterType=1&isSystem=1&tagId=0&tagFilterCount=0&template=publish&long_or_short=short'
        #     yield scrapy.Request(url=url,callback=self.parse_item)

    # def parse_item(self,response):
    #     results=response.text 
    #     for result in results:
    #         item=DangdangItem()
    #         item['comment']=result.css('.describe_detail')
    #         item['status']=result.css('.starline.clearfix')
    #         yield item


