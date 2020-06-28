# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bf
from maoyanmovie.items import MaoyanmovieItem
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        # for i in range(0, 10):
        i = 0
        url = f'https://maoyan.com/films?showType=3&offset={i * 30}'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_url = 'https://maoyan.com'
        title_list = Selector(response=response).xpath(
            '//div[@class="channel-detail movie-item-title"]')
        for film in title_list[:10]:
            title = film.xpath('./a/text()').extract()[0]
            # print(film.xpath('./a/@href').extract()[0])
            link = base_url + film.xpath('./a/@href').extract()[0]
            item = MaoyanmovieItem()
            item['title'] = title
            item['link'] = link
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)
            # yield item

    def parse2(self, response):
        item = response.meta['item']
        # soup = bf(response.text, 'html.parser')
        movies = Selector(response=response).xpath(
            '//div[@class="movie-brief-container"]/ul')
        plan_date = movies.xpath('./li[3]/text()').extract()[0]
        film_type_list = [str(i).strip() for i in movies.xpath('./li[1]/a/text()').extract()]
        film_type = ','.join(film_type_list)
        item['plan_date'] = plan_date
        item['film_type'] = film_type
        yield item
