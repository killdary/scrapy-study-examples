# -*- coding: utf-8 -*-

import scrapy
import logging



class CulturaSpider(scrapy.Spider):
    name='cultura'
    start_urls=[
        'https://www.livrariacultura.com.br/busca?N=102831&Ntt='
    ]
    pages = 2

    def parse(self, response):
        for livro in response.css('div.product-ev-box'):
            url_detail = livro.css('div.product-font-ev.product-title-ev > a::attr(href)').extract_first()
            url_detail = response.urljoin(url_detail)

            details = yield scrapy.Request(url=url_detail, callback=self.parse_deetaisl)

            yield {
                'titulo': livro.css('div.product-font-ev.product-title-ev > a::text').extract_first(),
                'author': livro.css('div.product-font-ev.author-title-ev > a::text').extract(),
                'price': livro.css('div.price-big-ev > b::text').extract_first(),
                'priceDiscount': livro.css('div.price-small-ev > b::text').extract_first(),
                'details': details
            }
        
        next_link = response.css('a.next')
        page_select = None
        if next_link is not None:
            for page in response.css('nav.sort > ul.pagination > li > a'):
                if page.css('::text').extract_first() == str(self.pages):
                    logging.info("#Extração dos dados da página: "+page.css('::text').extract_first())
                    page_select = page
                    self.pages += 1
                    break

            if page_select is not None:
                next_url = page_select.css('::attr(href)').extract_first()
                next_url = response.urljoin(next_url)
                yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_deetaisl(self, response):
        yield {
            'rated': response.css('#starRate meta::attr(content)').extract_first(),
            'avaliacoes': response.css('#starRate a span::text').extract_first(),
            'sinopse': response.css('div.container.product-details > div.content::text').extract_first(),
            'editora': response.css('#product-list-detail li:nth-child(1) ul li:nth-child(2) a::text').extract_first(),
            'assunto': response.css('#product-list-detail li:nth-child(1) ul li:nth-child(5) a::text').extract(),
            'idioma':  response.css('#product-list-detail li:nth-child(1) ul li:nth-child(6)::text').extract_first()
        }