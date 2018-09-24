# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.shell import inspect_response


class MainSpider(CrawlSpider):
    name = 'main'
    allowed_domains = ['www.chefkoch.de']
    start_urls = ['http://www.chefkoch.de/rezepte/kategorien']

    rules = (
        Rule(LinkExtractor(allow=r'/rs/.*'), follow=True),
        Rule(LinkExtractor(allow=r'/rezepte/.*\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        inspect_response(response, self)
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
