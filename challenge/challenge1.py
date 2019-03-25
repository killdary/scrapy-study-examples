# -*- coding: utf-8 -*-
import scrapy


class Challenge1Spider(scrapy.Spider):
    name = 'challenge1'

    start_urls = ['https://scrapingclub.com/exercise/detail_basic/']

    def parse(self, response):
        product = dict()

        product["title"] = response.xpath("//h3[@class='card-title']/text()").extract_first()
        product["price"] = response.xpath("//div[@class='card-body']/h4").extract_first()
        product["desc"] = response.xpath("//div[@class='card-body']/p[@class='card-text']").extract_first()

        yield {
            'product': product
        }