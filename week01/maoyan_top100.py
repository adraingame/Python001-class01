import requests
from bs4 import BeautifulSoup as bs
import lxml.etree
import time
import pandas as pd

# 爬取页面详细信息
# def get_url():
# 电影详细页面
base_url = 'https://maoyan.com'
url_top100 = 'https://maoyan.com/board/4'

# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

# 声明为字典使用字典的语法赋值
header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': '__mta=88979236.1592934830231.1593012971860.1593012973989.11; uuid_n_v=v1; uuid=7DA319E0B57A11EA8B56A5EC695B0A73B85FF15367D047B28AD8D931299AD0E5; _csrf=ac96431f26ee6d80a515e9299d2e0ed4dfba7aea034783756cfda03598e11acd; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=172e2509038c8-02e1b51b408629-31607402-fa000-172e2509038c8; _lxsdk=7DA319E0B57A11EA8B56A5EC695B0A73B85FF15367D047B28AD8D931299AD0E5; mojo-uuid=f875e2f935eac06342b889479fe44b9e; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1592934830,1593012758; __mta=88979236.1592934830231.1593011451298.1593012957924.7; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593012974; _lxsdk_s=172e76139c5-d94-9f4-1b3%7C%7C1',
'Host': 'maoyan.com',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'none',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'   
}
# header['user-agent'] = user_agent
response = requests.get(url_top100, headers=header)
# print(response)
bs_info = bs(response.text, 'html.parser')
urls = []
# time.sleep(10)
for tags in bs_info.find_all('div', class_ = 'movie-item-info'):
    for atag in tags.find_all('a',):
        # 获取所有链接
        url = base_url + atag.get('href')
        # print(url)
        urls.append(url)
        # 获取电影名字
        # print(atag.get('title'))

mylists = []
for url in urls:
    rep = requests.get(url, headers = header)

    # xml化处理
    selector = lxml.etree.HTML(rep.text)

    # 电影名称
    film_name = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/h1/text()')
    print(f'电影名称: {film_name[0]}')

    # 上映日期
    plan_date = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()')
    print(f'上映日期: {plan_date[0]}')

    # 类型
    film_types = selector.xpath("//*[@class = 'ellipsis']/a/text()")
    print(film_types) 

    mylist = [film_name[0], plan_date[0], film_types]
    mylists.append(mylist)


    

movie2 = pd.DataFrame(data = mylists)

    # windows需要使用gbk字符集
movie2.to_csv('./movie2.csv', encoding='utf8', index=False, header=['名称','上映日期','分类'])

