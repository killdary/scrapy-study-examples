# -*- codgig: utf-8 -*-
import scrapy


class QuoteSpider(scrapy.Spider):
    name = "quote1"
    start_urls = ["http://quotes.toscrape.com/page/1/"]

    def parse(self, response):
        for quote in response.css('div.quote'):
            author_url = quote.css('span > a::attr(href)').extract_first()
            author_url = response.urljoin(author_url)

            author = yield scrapy.Request(url=author_url, callback=self.parse_author)

            yield {
                'name': quote.css('span.text::text').extract_first(),
                'tags:': quote.css('a.tag::text').extract(),
                'author': author
            }

        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url);
            yield scrapy.Request(url=next_page_url, callback=self.parse)


    def parse_author(self, response):
        yield {
            'name': response.css('h3.author-title::text').extract_first(),
            'bonr': response.css('span.author-born-date::text').extract_first(),
            'location': response.css('span.author-born-location::text').extract_first(),
            'detail': response.css('div.author-description::text').extract_first()
        }
