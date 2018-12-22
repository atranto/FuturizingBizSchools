# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['www.glassdoor.com']
    start_urls = ['https://www.glassdoor.com/Reviews/netherlands-reviews-SRCH_IL.0,11_IN178.htm']

    def parse(self, response):
        for company in response.xpath('//*[@class = "eiHdrModule module snug "]'):
        	
        	yield {'Company name': company.xpath('.//*[@class = " margBotXs"]/a/text()').extract_first().lstrip(),
            	   'Overall rating': float(company.xpath('.//*[@class = "bigRating strong margRtSm h1"]/text()').extract_first().lstrip().replace(',','.')),
            	   'Percent recommendation': int(re.findall('\d+', company.xpath('.//*[@class = "minor hideHH margRtLg block margTopXs"]/text()').extract_first().lstrip())[0])/100,
            	   'Reviews count': company.xpath('.//*[@class = "eiCell cell reviews"]/*[@class = "num h2"]/text()').extract_first(),
            	   'Salaries': company.xpath('.//*[@class = "eiCell cell salaries"]/*[@class = "num h2"]/text()').extract_first(),
            	   'Interviews count': company.xpath('.//*[@class = "eiCell cell interviews"]/*[@class = "num h2"]/text()').extract_first(),
            	   'Website': company.xpath('.//*[@class = "webInfo"]/*[@class = "url"]/text()').extract_first(),
            	   'Location': company.xpath('.//*[@class = "hqInfo adr"]/*[@class = "value"]/text()').extract_first()}
        
        # follow links to company pages
        for href in response.xpath('//*[@class = " margBotXs"]/a/@href').extract():
            yield (response.follow(href, self.parse_company))

        next_page = response.xpath('//*[@class = "next"]/a/@href').extract_first()
        if next_page is not None:
            yield (response.follow(next_page, callback=self.parse))
        #next_page_url = response.xpath('//*[@class = "next"]/a/@href').extract_first()
        #absolute_next_page_url = response.urljoin(next_page_url) # To get the full working URL
        #yield (scrapy.Request(absolute_next_page_url))
    def parse_company(self, response):
        #item = scrapy.Item()
        yield{'Benefits': response.xpath('//*[@class = "eiCell cell benefits "]/*[@class = "num h2"]/text()').extract_first(),
              'Size': response.xpath('//*[@class = "infoEntity"]/*[@class = "value"]/text()').extract()[1],
              'Industry': response.xpath('//*[@class = "infoEntity"]/*[@class = "value"]/text()').extract()[4],
              'CEO percent approval': int(re.findall('\d+', response.xpath('//*[@id = "EmpStats_Approve"]').extract()[0])[0])/100}    
