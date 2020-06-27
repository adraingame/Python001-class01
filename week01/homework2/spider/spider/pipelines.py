# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class SpiderPipeline:

    mylists = []

    def process_item(self, item, spider):
        title = item['title']
        plan_date = item['plan_date']
        film_type = item['film_type']
        mylist = ['title', 'plan_date', 'film_type']

        mylists.append(mylist)
        return item

    movie = pd.DataFrame(data=mylists)
    movie.to_csv('./movie2.csv', encoding='utf8',
                 index=False, header=['名称', '上映日期', '分类'])
