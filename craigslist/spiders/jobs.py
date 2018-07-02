# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    #allowed_domains = ['https://newyork.craigslist.org/search/egr']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        jobs = response.css('p.result-info')
        for job in jobs:
            title = job.css('a.result-title.hdrlnk::text').extract_first()
            address = job.css('span.result-meta > span.result-hood::text').extract_first("")[2:-1]
            url = job.css('a[href*="craigslist.org"]::attr(href)').extract_first()

            yield Request(url,callback=self.parse_page,meta={'Url':url,'Title':title,'Address':address})
        next_page_url = response.css('a.button.next::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)

        yield Request(next_page_url,callback=self.parse)
    
    def parse_page(self,response):
        url = response.meta.get('Url')
        title = response.meta.get('Title')
        address = response.meta.get('Address')
        description = "".join(line for line in response.css('section#postingbody::text').extract())
        compensation = response.css('p.attrgroup > span > b::text')[0].extract()
        emp_type = response.css('p.attrgroup > span > b::text')[1].extract()

        yield {'Url':url,'Title':title,'Address':address,'Description':description,'Compensation':compensation,'Emp_type':emp_type}