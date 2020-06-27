学习笔记

# 爬虫流程

1. 选定目标url

   `url = 'https://maoyan.com'`

2. 模拟浏览器发送请求

   请求头模拟，需要根据实际情况去选择，user_agent一定要有，其余的如cookie需要根据目标网站的具体情况而定。

   ```python
   header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Cache-Control': 'max-age=0',
              'Connection': 'keep-alive',
              'Cookie': '__mta=88979236.1592934830231.1593179454664.1593179944446.12; uuid_n_v=v1; 	   uuid=7DA319E0B57A11EA8B56A5EC695B0A73B85FF15367D047B28AD8D931299AD0E5;    _csrf=ac96431f26ee6d80a515e9299d2e0ed4dfba7aea034783756cfda03598e11acd; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=172e2509038c8-02e1b51b408629-31607402-fa000-172e2509038c8; _lxsdk=7DA319E0B57A11EA8B56A5EC695B0A73B85FF15367D047B28AD8D931299AD0E5; mojo-uuid=f875e2f935eac06342b889479fe44b9e; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1592934830,1593012758,1593110954; mojo-session-id={"id":"a9b0bba94a952b945a38da0671189f7d","time":1593179443240}; __mta=88979236.1592934830231.1593179454664.1593179459207.12; mojo-trace-id=6; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593179944; _lxsdk_s=172f0e51112-771-85d-704%7C%7C7',
               'Host': 'maoyan.com',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-User': '?1',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
                 }
   ```

3. 得到响应

   需要用到第三方requests库，使用pip安装

   ```python
   pip install requests
   ```

   ```python
   import requests
   response = requests.get(url, headers=header)
   ```

   

4. 解析页面（html）

   使用BeautifulSoup解析页面，需要安装第三方的bs4库

   ```python
   pip install bs4
   ```

   ```python
   from bs4 import BeautifulSoup
   bs_info = bs(response.text, 'html.parser')
   ```

   使用lxml解析页面，需要安装第三方库lxml

   ```python
   pip install lxml
   ```

   ```python
   import lxml.etree
   selector = lxml.etree.HTML(rep.text)
   ```

5. 筛选爬取目标

   使用BeautifulSoup筛选爬取目标，使用find_all()，find()方法，结合浏览器的调试工具（快捷键F12）筛选相对应的标签，属性。获取属性使用get()方法，获取内容使用text

   ```python
   title_list = soup.find_all('p', attrs={'class': 'name'})
   for film in title_list:
   	title = film.find('a').get('title')
   ```

   使用lxml和xpath结合，使用浏览器的调试工具，筛选相对应的标签，属性。标签内容使用text()，属性使用@attrs

   ```python
   # 浏览器给出的绝对路径
   film_name = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/h1/text()')
   plan_date = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()')
   # xpath的相对路径
   film_types = selector.xpath("//*[@class = 'ellipsis']/a/text()")
   ```

6. 保存结果

   将结果输出到文本或者其他文件中。

   输出到文本可以用with open() as f:

7. 使用爬取结果进行后续处理

# scrapy框架

## 安装scrapy框架
```python
pip install scrapy
```
## 建立爬虫项目
```python
# project_name为自定义内容
scrapy startproject project_name
```
## 创建爬虫

爬虫文件生成在/project_name/project_name/spiders/目录中
```python
# spider_name为自定义内容，object.com为爬虫域
scrapy genspider spider_name object.com
```
## 运行爬虫
```
# 进入爬虫项目
cd project_name
# 运行爬虫
scrapy crawl spider_name
```

## scrapy目录结构
>scrapy.cfg: 项目的配置文件

>project_name/: 该项目的python模块。在此放入代码（核心）

>project_name/items.py: 项目中的item文件.（这是创建容器的地方，爬取的信息分别放到不同容器里，需要打开setting中的设置项）

>project_name/pipelines.py: 项目中的pipelines文件.

>project_name/settings.py: 项目的设置文件.（我用到的设置一下基础参数，比如加个文件头，设置一个编码）project_name/spiders/: 放置spider代码的目录. （放爬虫的地方）

## itmes的定义，items不是一开始定义好的，可以跟随项目一点点更新

```
import scrapy

class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    plan_date = scrapy.Field()
    film_type = scrapy.Field()
```
## setting设置项
```
# 模拟请求
USER_AGENT = 'spider (+http://www.yourdomain.com)'
```
```
# 延时处理
DOWNLOAD_DELAY = 3
```
- COOKIES_ENABLED = True，自动在后续的请求中添加响应的cookie，我们自己通过cookies设置的cookie会加入并覆盖到响应设置的cookie中
- COOKIES_ENABLED = False，通过cookies设置的，以及响应设置的cookie，全部无效。
- 想要设置自己的cookie，而不想添加任何 response 设置的多余的cookie，怎么办
经过测试，使用 headers 参数可以添加，我们把 COOKIES_ENABLED 设置为 False
```
COOKIES_ENABLED =False
```
```
# 打开此项pipline才会有相应的内容输出
ITEM_PIPELINES = {
   'spider.pipelines.SpiderPipeline': 300,
}
```
## scrapy框架的整体执行流程：
>1. spider的yeild将request发送给engine
>2. engine对request不做任何处理发送给scheduler
>3. scheduler，生成request交给engine
>4. engine拿到request，通过middleware发送给downloader
>5. downloader在\获取到response之后，又经过middleware发送给engine
>6. engine获取到response之后，返回给spider，spider的parse()方法对获取到的response进行处理，解析出items或者requests
>7. 将解析出来的items或者requests发送给engine
>8. engine获取到items或者requests，将items发送给ItemPipeline，将requests发送给scheduler（ps，只有调度器中不存在request时，程序才停止，及时请求失败scrapy也会重新进行请求）
