学习笔记

# 关于pipline写入mysql
知乎上的一遍文章写得非常的简洁
https://zhuanlan.zhihu.com/p/68149801

使用scrapy爬取网站数据，是一个目前来说比较主流的一个爬虫框架，也非常简单。

1、创建好项目之后现在settings.py里面把ROBOTSTXT_OBEY的值改为False，不然的话会默认遵循robots协议，你将爬取不到任何数据。

2、在爬虫文件里开始写你的爬虫，你可以使用xpath，也可以使用css选择器来解析数据，等将数据全部解析完毕之后再items文件里面去声明你的字段

```python
import scrapy
class JobspiderItem(scrapy.Item):
    zwmc = scrapy.Field()
    zwxz = scrapy.Field()
    zpyq = scrapy.Field()
    gwyq = scrapy.Field()
```
3、然后再爬虫文件里面先去导入items里面声明字段的类，接着创建item对象，写入值，最后别忘了把item给yield出去

```python
item = JobspiderItem()
item['zwmc'] = zwmc
item['zwxz'] = money
item['zpyq'] = zpyq
item['gwyq'] = gzyq
yield item
```
4、接下来就是存入mysql数据库了：

1.在pipelings.py文件里面先导入item类以及pymysql模块
```python
from ..jobspider.items import JobspiderItem
import pymysql
```
2.然后就开始连接数据库以及写入数据库，我这里是直接先将mysql数据库以及数据表建立好了，并没有在代码里面创建
```python
class JobspiderPipeline(object):
    def __init__(self):
        # 1. 建立数据库的连接
        self.connect = pymysql.connect(
	    # localhost连接的是本地数据库
            host='localhost',
            # mysql数据库的端口号
            port=3306,
            # 数据库的用户名
            user='root',
            # 本地数据库密码
            passwd='123456',
            # 表名
            db='job51',
            # 编码格式
            charset='utf8'
        )
        # 2. 创建一个游标cursor, 是用来操作表。
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # 3. 将Item数据放入数据库，默认是同步写入。
        insert_sql = "INSERT INTO job(zwmc, zwxz, zpyq, gwyq) VALUES ('%s', '%s', '%s', '%s')" % (item['zwmc'], item['zwxz'], item['zpyq'], item['gwyq'])
        self.cursor.execute(insert_sql)

        # 4. 提交操作
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
```
5、最后就是去settings.py文件里面将ITEM_PIPELINES给解注释了

# 关于github上代理池
时间关系，没有使用代理池的API，直接使用了老师的处理方式

# 关于模拟登陆
输入用户名密码后还会碰到拖动滑块拼图，点击对应的文字，需要图形处理的技术积累


这周的课程让我感觉到做好爬虫还需要很多技术积累

## 简单的模拟登陆
需要selenium中的webdriver模块
selenium模块需要pip安装
```
pip install selenium
```
导入webdriver
```python
form selenium import webdriver
```
webdriver需要下载对应浏览器，对应版本的驱动，并放到指定目录（可以放到python的安装目录）
调用webdriver
'''python
browser = webdriver.Chrome()
url = 'https://www.douban.com'
browser.get(url)
'''
找到登陆用户名密码的元素find_element_by_xpath()，使用send_keys()传输数据
```python
browser.find_element_by_xpath('//input[@name="mobileOrEmail"]').send_keys('raingame@163.com')
```
找到登陆按钮，模拟点击click()
```python
browser.find_element_by_xpath('//input[@name="mobileOrEmail"]').click()
```
获取cookies
```python
cookies = browser.get_cookies()
```
关闭浏览器
```python
brower.close()
```