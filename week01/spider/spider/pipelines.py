# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class SpiderPipeline:

    def process_item(self, item, spider):
        title = item['title']
        link = item['link']
        plan_date = item['plan_date']
        film_type = item['film_type']
        output = f'|{title}|\t|{link}|\t|{plan_date}|\t|{film_type}|\n\n'
        with open('E:\\a.txt', 'a+', encoding='utf-8') as article:
            article.write(output)
        # # mylist = ['title', 'link', 'plan_date', 'film_type']
        # # mylists = []
        # # mylists.append(mylist)

        # # movie = pd.DataFrame(data=mylists)

        return item
