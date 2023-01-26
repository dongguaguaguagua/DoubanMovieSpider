import json
import os
from bs4 import BeautifulSoup, NavigableString, Comment
import requests
import re
import datetime

'''
    查看IP：
    http://icanhazip.com/
'''

# # 电影名称
# name=[]
# # 海报链接
# post_link=[]
# # 上映年份
# year=[]
# # 豆瓣评分
# rating=[]
# # 评分个数
# rating_people=[]
# # 短评数
# short_rating_num=[]
# # 影评数
# review_num=[]
# # 电影时长
# movie_length=[]
# # 上映日期
# release_date=[]
# # 导演
# director=[]
# # 演员
# actors=[]
# # 编剧
# playwright=[]
# # 体裁
# genre=[]
# # 国家
# country=[]

# 解析
def update_data(soup):
    tmp = re.findall(r"\d+\.?\d*",str(soup.find('span',class_='year')))
    if(tmp == []):
        year="unknown"
    else:
        year=tmp[0]
    # 电影名称
    if(soup.findAll(property="v:itemreviewed")!=[]):
        name=soup.findAll(property="v:itemreviewed")[0].text
    else:
        name="unknown"
    # 海报链接
    if(soup.find(rel="v:image")!=None):
        post_link=soup.find(rel="v:image").get('src').replace("s_ratio_poster","raw").replace("webp","jpg")
    else:
        post_link="None"

    # 豆瓣评分
    if(soup.findAll(property="v:average")!=[]):
        if(soup.findAll(property="v:average")[0].text!=""):
            rating=soup.findAll(property="v:average")[0].text
        else:
            rating='0'
    else:
        rating='0'
    # 评分个数
    if(soup.find('a',class_="rating_people")!=None):
        rating_people=re.findall(r"\d+\.?\d*",str(soup.find('a',class_="rating_people")))[0]
    else:
        rating_people='0'

    # 短评数
    if(soup.find(id="comments-section")!=None):
        short_rating_num=re.findall(r"\d+\.?\d*",soup.find(id="comments-section").div.h2.span.a.text)[0]
    else:
        short_rating_num="0"
    # 影评数
    if(soup.find(href="reviews")!=None):
        review_num=re.findall(r"\d+\.?\d*",soup.find(href="reviews").text)[0]
    else:
        review_num="0"
    # 电影时长
    if(soup.findAll(property="v:runtime")!=[]):
        movie_length=soup.findAll(property="v:runtime")[0].text
    else:
        movie_length='unknown'
    # 上映日期
    if(soup.findAll(property="v:initialReleaseDate")!=[]):
        release_date=soup.findAll(property="v:initialReleaseDate")[0].text
    else:
        release_date='unknown'
    # 导演
    if(soup.findAll(text="导演")!=[]):
        director=soup.findAll(text="导演")[0].next.next.text
    else:
        director='unknown'
    # 编剧
    if(soup.findAll(text="编剧")!=[]):
        playwright=soup.findAll(text="编剧")[0].next.next.text
    else:
        playwright='unknown'
    # 演员
    if(soup.findAll('span',class_="actor")!=[]):
        actors=soup.findAll('span',class_="actor")[0].text.replace("主演: ","")
    else:
        actors='unknown'
    # 体裁
    if(soup.find_all(property="v:genre")!=[]):
        genre=BeautifulSoup(' / '.join(str(soup.find_all(property="v:genre")).split('</span>, <span property="v:genre">')),'lxml').findAll('span')[0].text
    else:
        genre='unknown'
    # 国家
    if(soup.findAll(text="制片国家/地区:")!=[]):
        country=soup.findAll(text="制片国家/地区:")[0].next.strip()
    else:
        country='unknown'
    return name+","+post_link+","+year+","+rating+","+rating_people+","+short_rating_num+","+review_num+","+movie_length+","+release_date+","+director+","+playwright+","+actors+","+genre+","+country


def get_proxy(choice='http'):
    #芝麻ip时间选优算法
    # 获取芝麻代理ip
    with open("proxy_api.txt","r") as file:
        url=file.read().strip()
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

    elif(ip_data['code']==116):
        print("获取ip失败,今日套餐已用完");
        return {"status":0}
    elif(ip_data['code']==111):
        print("获取ip失败,请求过快");
        return {"status":0}
    proxyMeta = "http://%(host)s:%(port)s" % {
        "host" : excellent_ip,
        "port" : excellent_ip_port,
    }
    proxies = {
        "http"  : proxyMeta,
        "https"  : proxyMeta
    }
    print(proxies)
    print("选择ip成功")
    return proxies


