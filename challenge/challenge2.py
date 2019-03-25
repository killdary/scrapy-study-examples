# -*- coding: utf-8 -*-
import scrapy
import re
import json


class Challenge2(scrapy.Spider):
    name='challenge2'
    start_urls=['https://scrapingclub.com/exercise/detail_json/']

    def parse(self, response):
        data = re.findall('var obj = ({[\s|\S]*});\n', response.body.decode("utf-8"), re.S)
        product = json.loads(data[0].replace('" + "', ''))
        del(product['img_path'])

        yield {
            'product': product
        }