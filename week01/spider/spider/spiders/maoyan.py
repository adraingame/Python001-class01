import scrapy
from bs4 import BeautifulSoup as bf
from spider.items import SpiderItem
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4']

    def start_requests(self):
        for i in range(0, 10):
            url = f'https://maoyan.com/board/4?offset={i * 10}'
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        base_url = 'https://maoyan.com'
        # items = []
        # soup = bf(response.text, 'html.parser')
        # title_list = soup.find_all('p', attrs={'class': 'name'})
        title_list = Selector(response=response).xpath('//p[@class="name"]')
        # title_list = response.xpath('//p[@class="name"]')
        for film in title_list:
            
            # title = film.find('a').get('title')
            title = film.xpath('./a/@title')
            # link = base_url + film.find('a').get('href')
            link = base_url + film.xpath('./a/@href')
            item = SpiderItem()
            item['title'] = title
            item['link'] = link
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)
            # yield item

    def parse2(self, response):
        item = response.meta['item']
        # soup = bf(response.text, 'html.parser')
        movies = Selector(response=response).xpath('//div[@class="movie-brief-container"]/ul')
        # plan_date = soup.find_all('li', attrs={'class': 'ellipsis'})[2].text
        plan_date = movies.xpath('./li[1]/a/text()')
        # film_type = soup.find_all('li', attrs={'class': 'ellipsis'})[0].text.replace('\n', ' ')
        film_type = movies.xpath('./li[3]/text()')
        item['plan_date'] = plan_date
        item['film_type'] = film_type
        yield item
