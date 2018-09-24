# -*- coding: utf-8 -*-
import unicodedata

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser


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
        amounts = response.xpath(r"//table[@class='incredients']/tr/td[@class='amount']/text()")
        amounts = [unicodedata.normalize("NFKC", amt).strip() for amt in amounts.extract()]
        i['amounts'] = amounts

        ingredients = response.xpath(r"//table[@class='incredients']/tr/td[@class='amount']/following-sibling::td//text()")
        ingredients = [ing.strip() for ing in ingredients.extract() if ing.strip()]
        i['ingredients'] = ingredients

        i['title'] = response.xpath(r"//h1[@class='page-title']/text()").extract_first()

        votes = response.xpath(r"//span[contains(@class, 'total-votes')]/text()")
        if votes:
            votes = votes.extract_first().strip("()")
            i['votes'] = int(votes)
        else:
            i['votes'] = 0

        if i['votes'] > 0:
            score = response.xpath(r"//span[contains(@class, 'average-rating')]/text()")
            i['score'] = float(score.extract_first()[1:]
                                    .replace(",", "."))
        else:
            i['score'] = None
        return i
