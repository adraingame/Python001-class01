'''
版本说明：Python训练营第一周作业一，相比ver1.0，2.0版本用函数将获取链接和页面详情进行了封装
描述：安装并使用 requests、bs4 库，爬取猫眼电影的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
作者：刘鹤东
版本号：ver2.0
'''


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# 爬取电影所有链接
def get_url():
    # 猫眼电影的url
    base_url = 'https://maoyan.com'
    url_sort = 'https://maoyan.com/films?showType=3&sortId=1'

    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

    # 声明为字典使用字典的语法赋值
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Cache-Control': 'max-age=0',
              'Connection': 'keep-alive',
              'Cookie': '__mta=88979236.1592934830231.1593179454664.1593179944446.12; uuid_n_v=v1; uuid=7DA319E0B57A11EA8B56A5EC695B0A73B85FF15367D047B28AD8D931299AD0E5; _csrf=ac96431f26ee6d80a515e9299d2e0ed4dfba7aea034783756cfda03598e11acd; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=172e2509038c8-02e1b51b408629-31607402-fa000-172e2509038c8; _lxsdk=7DA319E0B57A11EA8B56A5EC695B0A73B85FF15367D047B28AD8D931299AD0E5; mojo-uuid=f875e2f935eac06342b889479fe44b9e; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1592934830,1593012758,1593110954; mojo-session-id={"id":"a9b0bba94a952b945a38da0671189f7d","time":1593179443240}; __mta=88979236.1592934830231.1593179454664.1593179459207.12; mojo-trace-id=6; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593179944; _lxsdk_s=172f0e51112-771-85d-704%7C%7C7',
              'Host': 'maoyan.com',
              'Sec-Fetch-Dest': 'document',
              'Sec-Fetch-Mode': 'navigate',
              'Sec-Fetch-Site': 'none',
              'Sec-Fetch-User': '?1',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
              }
    response = requests.get(url_sort, headers=header)
    # print(response.text)
    bs_info = bs(response.text, 'html.parser')
    urls = []
    # # time.sleep(10)
    for tags in bs_info.find_all('div', class_='channel-detail movie-item-title'):
        for atag in tags.find_all('a',):
            # 获取所有链接
            url = base_url + atag.get('href')
            # print(url)
            urls.append(url)
    #         # 获取电影名字
    #         # print(atag.get('title'))
    return urls

# 获取详情页面
def get_film_attrs(url):
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Cache-Control': 'max-age=0',
              'Connection': 'keep-alive',
              'Cookie': '__mta=88979236.1592934830231.1593179454664.1593179944446.12; uuid_n_v=v1; uuid=7DA319E0B57A11EA8B56A5EC695B0A73B85FF15367D047B28AD8D931299AD0E5; _csrf=ac96431f26ee6d80a515e9299d2e0ed4dfba7aea034783756cfda03598e11acd; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=172e2509038c8-02e1b51b408629-31607402-fa000-172e2509038c8; _lxsdk=7DA319E0B57A11EA8B56A5EC695B0A73B85FF15367D047B28AD8D931299AD0E5; mojo-uuid=f875e2f935eac06342b889479fe44b9e; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1592934830,1593012758,1593110954; mojo-session-id={"id":"a9b0bba94a952b945a38da0671189f7d","time":1593179443240}; __mta=88979236.1592934830231.1593179454664.1593179459207.12; mojo-trace-id=6; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593179944; _lxsdk_s=172f0e51112-771-85d-704%7C%7C7',
              'Host': 'maoyan.com',
              'Sec-Fetch-Dest': 'document',
              'Sec-Fetch-Mode': 'navigate',
              'Sec-Fetch-Site': 'none',
              'Sec-Fetch-User': '?1',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
              }
    rep = requests.get(url, headers=header)
    bs_rep = bs(rep.text, 'html.parser')
    film_name = (bs_rep.find_all('h1', attrs={'class': 'name'}))[0].text
    print(film_name)
    plan_date = (bs_rep.find_all('li', attrs={'class': 'ellipsis'}))[2].text
    print(plan_date)
    film_type = (bs_rep.find_all('li', attrs={'class': 'ellipsis'}))[0].text
    print(film_type)

    mylist = [film_name, plan_date, film_type]
    return mylist


urls = get_url()

mylists = []
for url in urls[:10]:
    time.sleep(5)
    mylist = get_film_attrs(url)
    mylists.append(mylist)


movie2 = pd.DataFrame(data=mylists)

# windows需要使用gbk字符集
movie2.to_csv('./movie2.csv', encoding='utf8',
              index=False, header=['名称', '上映日期', '分类'])
