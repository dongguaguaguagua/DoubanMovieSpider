# -*- coding: utf-8 -*-
import requests
import json
import random
import datetime
from bs4 import BeautifulSoup
import re
import pandas
import time

# 电影名称
name=[]
# 海报链接
post_link=[]
# 上映年份
year=[]
# 豆瓣评分
rating=[]
# 评分个数
rating_people=[]
# 短评数
short_rating_num=[]
# 影评数
review_num=[]
# 电影时长
movie_length=[]
# 上映日期
release_date=[]
# 导演
director=[]
# 演员
actors=[]
# 编剧
playwright=[]
# 体裁
genre=[]
# 国家
country=[]

def update_data(soup):
    # 解析
    # 上映日期
    year.append(re.findall(r"\d+\.?\d*",str(soup.find('span',class_='year')))[0])
    # 电影名称
    name.append(soup.findAll(property="v:itemreviewed")[0].text)
    # 海报链接
    post_link.append(soup.find(rel="v:image").get('src').replace("s_ratio_poster","raw").replace("webp","jpg"))
    # 豆瓣评分
    if(soup.findAll(property="v:average")[0].text!=''):
        rating.append(soup.findAll(property="v:average")[0].text)
    else:
        rating.append('0')
    # 评分个数
    if(soup.find('a',class_="rating_people")!=None):
        rating_people.append(re.findall(r"\d+\.?\d*",str(soup.find('a',class_="rating_people")))[0])
    else:
        rating_people.append('0')
    # 短评数
    short_rating_num.append(re.findall(r"\d+\.?\d*",soup.find('div',class_="mod-hd").find_all("a")[1].text)[0])
    # 影评数
    review_num.append(re.findall(r"\d+\.?\d*",soup.find(href="reviews").text)[0])
    # 电影时长
    if(soup.findAll(property="v:runtime")!=[]):
        movie_length.append(soup.findAll(property="v:runtime")[0].text)
    else:
        movie_length.append('None')
    # 上映日期
    if(soup.findAll(property="v:initialReleaseDate")!=[]):
        release_date.append(soup.findAll(property="v:initialReleaseDate")[0].text)
    else:
        release_date.append('unknown')
    # 导演
    if(soup.findAll(text="导演")!=[]):
        director.append(soup.findAll(text="导演")[0].next.next.text)
    else:
        director.append('unknown')
    # 编剧
    if(soup.findAll(text="编剧")!=[]):
        playwright.append(soup.findAll(text="编剧")[0].next.next.text)
    else:
        playwright.append('unknown')
    # 演员
    if(soup.findAll('span',class_="actor")!=[]):
        actors.append(soup.findAll('span',class_="actor")[0].text.replace("主演: ",""))
    else:
        actors.append('unknown')
    # 体裁
    if(soup.find_all(property="v:genre")!=[]):
        genre.append(BeautifulSoup(' / '.join(str(soup.find_all(property="v:genre")).split('</span>, <span property="v:genre">')),'lxml').findAll('span')[0].text)
    else:
        genre.append('unknown')
    # 国家
    if(soup.findAll(text="制片国家/地区:")!=[]):
        country.append(soup.findAll(text="制片国家/地区:")[0].next.strip())
    else:
        country.append('unknown')


def get_proxy(choice='http'):
    #芝麻ip时间选优算法
    # 获取芝麻代理ip
    url = "http://webapi.http.zhimacangku.com/getip?num=10&type=2&pro=&city=0&yys=0&port=1&pack=290010&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions="
    # url选择json
    body = {}
    headers = {}
    response = requests.post(url, json=body, headers=headers)
    ip_data = response.json()
    if(ip_data['code']==0):
        print("获取ip成功")
        #每次读取10条记录对比，芝麻ip每日免费20个
        global excellent_ip
        global excellent_ip_port
        new_data=ip_data
        member = []
        #建立数据入口
        date1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        d1 = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
        for geshu, val1 in enumerate(ip_data['data']):
            #获得ip个数geshu
            # print(new_data['data'][geshu])
           # 将每个时间转换为时间戳加入新数组
            new_time=new_data['data'][geshu]['expire_time']
            d2 =datetime.datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S')
            d = d2-d1
            sec= format(d.seconds);#获取秒数
            sec=int(sec)
            member.append(sec)

        # 冒泡排序
        member.sort(reverse=True)
        #对比得到该时间的ip
        for geshu2, val2 in enumerate(ip_data['data']):
            #获得ip个数geshu
            new_time2=new_data['data'][geshu2]['expire_time']
            d2 =datetime.datetime.strptime(new_time2, '%Y-%m-%d %H:%M:%S')
            d = d2-d1
            #减去固定的时间点
            sec= format(d.seconds);#获取秒数
            sec=int(sec)
            if(sec==member[0]):
                excellent_ip=new_data['data'][geshu2]['ip']
                excellent_ip_port=new_data['data'][geshu2]['port']
                # TODO: write code...
        # TODO: write code...
    else:
        print("获取ip失败");

    proxyMeta = "http://%(host)s:%(port)s" % {
        "host" : excellent_ip,
        "port" : excellent_ip_port,
    }
    proxies = {
        "http"  : proxyMeta,
        "https"  : proxyMeta
    }
    print("选择ip成功")
    return proxies



def get_user_agent():
    """
    得到随机user-agent
    :return:
    """
    user_agents = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    user_agent = random.choice(user_agents)
    return user_agent

if __name__ == "__main__":
    with open("/Users/huzongyu/大学/数据世界探秘/moviedata/dic1.json","r") as file:
        data=json.load(file)
    proxies=get_proxy()
    headers = {'User-Agent': get_user_agent()}
    for i in range(10):
        # if(i%20==1):
        #     proxies=get_proxy()
        #     headers = {'User-Agent': get_user_agent()}
        resp = requests.get("http://www.douban.com/subject/"+str(data[str(i)]), proxies=proxies,headers=headers)
        soup=BeautifulSoup(resp.text, 'lxml')
        print("生成第",i,"个电影数据……")
        update_data(soup)
        time.sleep(random.random()*3)

    data=pandas.DataFrame({"name":name,"post_link":post_link,"year":year,"rating":rating,"rating_people":rating_people,"short_rating_num":short_rating_num,"review_num":review_num,"movie_length":movie_length,"release_date":release_date,"director":director,"actors":actors,"playwright":playwright,"genre":genre,"country":country})
    print("正在导入csv……")
    data.to_csv("MyMovieData.csv",index=False,sep=',',encoding='utf8')
    print("csv文件生成成功")

