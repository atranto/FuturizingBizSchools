# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

class Test2Spider(scrapy.Spider):
    name = 'test2'
    start_urls = ['https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK']

    def parse(self, response):
    	#return [FormRequest(url="https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK",
        #            formdata={'name': 'toanh260196@gmail.com', 'password': 'anhnguyenngoc'},
        #            callback=self.after_login)]
    	return scrapy.FormRequest.from_response(
            response,
            formdata={'username': '###', 'password': '###'},
            callback=self.after_login
        )
    	#token = response.xpath('//*[@id="InlineLoginModule"]/div/div/div[1]/div[2]/div[2]/form/input[1]')
    	#return FormRequest.from_response(response, formdata={'gdToken': token,'username': 'toanh260196@gmail.com', 'password': 'anhnguyenngoc'},
        #								  callback=self.after_login)

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return
        else:
        	return Request(url="https://www.glassdoor.com/Reviews/netherlands-reviews-SRCH_IL.0,11_IN178.htm", callback=self.parse_reviews)

    def parse_reviews(self, response):
        # follow links to company pages
        for href in response.xpath('//*[@class = "eiCell cell reviews"]/@href').extract():
            yield (response.follow(href, self.parse_company1))

    def parse_company1(self, response):
    	for review in response.xpath('//*[@class = " empReview cf "]/@id').extract():
        	xpath1 = '//*[@id="{}"]/div/div[2]/div/div[2]/div/div[1]/span/div/ul/li[1]/span/@title'.fomat(review)
        	xpath2 = '//*[@id="{}"]/div/div[2]/div/div[2]/div/div[1]/span/div/ul/li[2]/span/@title'.fomat(review)
        	xpath3 = '//*[@id="{}"]/div/div[2]/div/div[2]/div/div[1]/span/div/ul/li[3]/span/@title'.fomat(review)
        	xpath4 = '//*[@id="{}"]/div/div[2]/div/div[2]/div/div[1]/span/div/ul/li[4]/span/@title'.fomat(review)
        	xpath5 = '//*[@id="{}"]/div/div[2]/div/div[2]/div/div[1]/span/div/ul/li[5]/span/@title'.fomat(review)
        	yield {'Company name': response.xpath('//*[@class = " strong tightAll"]/@data-company').extract_first(), 
        		   'Work/Life Balance': review.xpath(xpath1).extract_first(),
        		   'Culture & Values': review.xpath(xpath2).extract_first(),
        		   'Career Opportunities': review.xpath(xpath3).extract_first(),
        		   'Comp & Benefits:': review.xpath(xpath4).extract_first(),
        		   'Senior Management': review.xpath(xpath5).extract_first()}