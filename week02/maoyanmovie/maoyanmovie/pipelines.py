# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

dbInfo = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'liuguoer@030126',
    'db': 'maoyanmovie'
}


class MaoyanmoviePipeline:
    def __init__(self):
        # 1. 建立数据库的连接
        self.connect = pymysql.connect(
	        # localhost连接的是本地数据库
            host=dbInfo['host'],
            # mysql数据库的端口号
            port=dbInfo['port'],
            # 数据库的用户名
            user=dbInfo['user'],
            # 本地数据库密码
            passwd=dbInfo['password'],
            # 表名
            db=dbInfo['db'],
            # 编码格式
            charset='utf8mb4'
        )
        # 2. 创建一个游标cursor, 是用来操作表。
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # 3. 将Item数据放入数据库，默认是同步写入。
        insert_sql = "INSERT INTO maoyanmovie(title, plan_date, type) VALUES ('%s', '%s', '%s')" % (item['title'], item['plan_date'], item['film_type'])
        self.cursor.execute(insert_sql)
        # 4. 提交操作
        self.connect.commit()
        # title = item['title']
        # plan_date = item['plan_date']
        # film_type = item['film_type']
        # output = f'{title}, {plan_date}, {film_type}\n'
        # with open('./maoyanmovie.csv', 'a+', encoding='utf-8') as article:
        #     article.write(output)
        #     article.close()
        return item
        
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
