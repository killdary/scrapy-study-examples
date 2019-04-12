# -*- coding: utf-8 -*-
import scrapy

class Challenge3Spider(scrapy.Spyder):
    name = 'challenge3'
    start_urls = [
        'https://scrapingclub.com/exercise/list_basic/'
    ]

    def parse(self, response):
        for card in response.css('.card-body'):
            link = card.css('h4 > a::attr(href)').extract_first()
            link = response.urljoin(link)

            details = yield scrapy.Request(url=link, callback=self.parse_details)

            yield {
                'title': card.css('h4 > a::text').extract_first(),
                'price': card.css('h4 > a::attr(href)').extract_first(),
                'details': details
            }
        next_page = response.css('a.page-link::attr(href)').extract_first()

    def parse_details(self, response):
        pass