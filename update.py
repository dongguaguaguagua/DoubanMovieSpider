import json
import os
from time import sleep
from bs4 import BeautifulSoup, NavigableString, Comment
import requests
import re
import datetime
import sys
'''
查看IP：
http://icanhazip.com/
查看是否高匿：
http://httpbin.org/get
'''

'''
电影名称: name
海报链接: post_link
上映年份: year
豆瓣评分: rating
评分个数: rating_people
短评数: short_rating_num
影评数: review_num
电影时长: movie_length
上映日期: release_date
导演: director
演员: actors
编剧: playwright
体裁: genre
国家: country
'''
# 解析
def update_data(soup):
    tmp = re.findall(r"\d+\.?\d*",str(soup.find('span',class_='year')))
    if(tmp == []):
        year="unknown"
    else:
        year=tmp[0]

    info=soup.find(id="info")
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
    if(info.findAll(property="v:runtime")!=[]):
        movie_length=info.findAll(property="v:runtime")[0].text
    else:
        movie_length='unknown'
    # 上映日期
    if(info.findAll(property="v:initialReleaseDate")!=[]):
        release_date=info.findAll(property="v:initialReleaseDate")[0].text
    else:
        release_date='unknown'
    # 导演
    if(info.findAll(text="导演")!=[]):
        director=info.findAll(text="导演")[0].next.next.text
    else:
        director='unknown'
    # 编剧
    if(info.findAll(text="编剧")!=[]):
        playwright=info.findAll(text="编剧")[0].next.next.text
    else:
        playwright='unknown'
    # 演员
    if(info.findAll('span',class_="actor")!=[]):
        actors=info.findAll('span',class_="actor")[0].text.replace("主演: ","")
    else:
        actors='unknown'

    # 体裁
    if(info.find_all(property="v:genre")!=[]):
        genre=BeautifulSoup(' / '.join(str(info.find_all(property="v:genre")).split('</span>, <span property="v:genre">')),'lxml').findAll('span')[0].text
    else:
        genre='unknown'
    # 国家
    if(info.findAll(text="制片国家/地区:")!=[]):
        country=info.findAll(text="制片国家/地区:")[0].next.strip()
    else:
        country='unknown'
    return name+","+post_link+","+year+","+rating+","+rating_people+","+short_rating_num+","+review_num+","+movie_length+","+release_date+","+director+","+playwright+","+actors+","+genre+","+country

# 青果代理
def get_qg_proxy(choice='http'):
    with open("proxy_api.txt","r") as file:
        url=file.read().strip()
    response = requests.post(url, headers={})
    ip_data = response.json()
    print(ip_data)
    if(ip_data['Code']==0):
        print("获取ip成功")
        proxyAddr=ip_data['Data'][0]['host']
        Authkey="CEBC9918"
        Authpwd="B24AE2729C9B"

        proxyMeta = "http://%(user)s:%(password)s@%(server)s" % {
            "user" : Authkey,
            "password" : Authpwd,
            "server" : proxyAddr
        }
        proxies = {
            "http"  : proxyMeta,
            "https"  : proxyMeta
        }
        return proxies
    elif(ip_data['code']==-11):
        print("获取ip失败,计划不存在或已过期");
        sys.exit(1)

    elif(ip_data['code']==-103):
        print("获取ip失败,资源不足");
        sys.exit(1)

    # elif(ip_data['code']==-11):
    #     print("获取ip失败,请求过快");
    #     return {"status":0}

# 芝麻代理
def get_zm_proxy(choice='http'):
    #芝麻ip时间选优算法
    # 获取芝麻代理ip
    with open("proxy_api.txt","r") as file:
        url=file.read().strip()
    # url选择json
    headers = {}
    json={}
    response = requests.post(url, json=json,headers=headers)
    ip_data = response.json()
    if(ip_data['code']==0):
        print("获取ip成功")

    # url选择json
    headers = {}
    response = requests.post(url, headers=headers)
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

        proxyMeta = "http://%(host)s:%(port)s" % {
            "host" : excellent_ip,
            "port" : excellent_ip,
        }
        proxies = {
            "http"  : proxyMeta,
            "https"  : proxyMeta
        }
        print(excellent_ip,excellent_ip)
        print(proxies)
        return proxies

    elif(ip_data['code']==116):
        print("获取ip失败,今日套餐已用完");
        sys.exit(1)

    # elif(ip_data['code']==111):
    #     print("获取ip失败,请求过快");
    #     sys.exit(1)

def update_json(soup):
    json=soup.find(type="application/ld+json").text
    return json


