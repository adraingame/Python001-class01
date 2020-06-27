'''
版本说明：Python训练营第一周作业一，使用scrapy爬取猫眼电影的前 10 个电影名称。由于IP被封，公司电脑的IP已经被猫眼禁掉，代码还未经过调试，xpath的路径已经在浏览器调试过
描述：使用 Scrapy 框架和 XPath 抓取猫眼电影的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
要求：必须使用 Scrapy 框架及其自带的 item pipeline、选择器功能，不允许使用 bs4 进行页面内容的筛选。
作者：刘鹤东
版本号：ver1.0
'''

import scrapy
from bs4 import BeautifulSoup as bf
from spider.items import SpiderItem
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        # for i in range(0, 10):
        i = 0
        url = f'https://maoyan.com/films?showType=3&offset={i * 30}'
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        base_url = 'https://maoyan.com'
        title_list = Selector(response=response).xpath(
            '//div[@class="channel-detail movie-item-title"]')
        for film in title_list[:10]:
            title = film.xpath('./a/text()')
            link = base_url + film.xpath('./a/@href')
            item = SpiderItem()
            item['title'] = title
            item['link'] = link
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta['item']
        # soup = bf(response.text, 'html.parser')
        movies = Selector(response=response).xpath(
            '//div[@class="movie-brief-container"]/ul')
        plan_date = movies.xpath('./li[1]/a/text()')
        film_type = movies.xpath('./li[3]/text()')
        item['plan_date'] = plan_date
        item['film_type'] = film_type
        yield item
