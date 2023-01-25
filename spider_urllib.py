# -*- coding: utf-8 -*-
import requests
import json
import random
import datetime
from bs4 import BeautifulSoup
import re
import pandas
import time
from fake_useragent import UserAgent
import urllib.request

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
    tmp = re.findall(r"\d+\.?\d*",str(soup.find('span',class_='year')))
    if tmp == []:
        year.append("unknown")
    else:
        year.append(tmp[0])
    # 电影名称
    name.append(soup.findAll(property="v:itemreviewed")[0].text)
    # 海报链接
    if(soup.find(rel="v:image")!=[]):
        post_link.append(soup.find(rel="v:image").get('src').replace("s_ratio_poster","raw").replace("webp","jpg"))
    else:
        year.append("None")
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
        movie_length.append('unknown')
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
    url = "http://webapi.http.zhimacangku.com/getip?num=10&type=2&pro=&city=0&yys=0&port=1&time=1&ts=1&ys=0&cs=1&lb=1&sb=0&pb=4&mr=1&regions="
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
    print(proxies)
    print("选择ip成功")
    return proxies


if __name__ == "__main__":
    with open("dic1.json","r") as file:
        data=json.load(file)
    proxies=get_proxy()
    print("获取代理成功")
    ua=UserAgent()
    headers = [('User-Agent', ua.random),('Referer',"https://movie.douban.com"),('Cennection','keep-alive')]

    for i in range(100):
        if(i%20==1):
            # 更新proxy
            proxies = get_proxy()
            print("更新proxy完成")

        # 传递proxy
        proxy_handler = urllib.request.ProxyHandler(proxies)
        opener = urllib.request.build_opener(proxy_handler)

        # 设置请求头
        print("正在请求……")
        opener.addheaders = headers
        resp = opener.open("https://www.douban.com/subject/"+str(data[str(i)]))
        print("请求成功")
        soup = BeautifulSoup(resp.read().decode("utf8",'ignore'), 'lxml')
        # if resp.status_code != 200:
        #     print("status_code : ",resp.status_code)
        #     continue
        print("生成第",i,"个电影数据……")
        update_data(soup)
        time.sleep(random.random()*3)

    data=pandas.DataFrame({"name":name,"post_link":post_link,"year":year,"rating":rating,"rating_people":rating_people,"short_rating_num":short_rating_num,"review_num":review_num,"movie_length":movie_length,"release_date":release_date,"director":director,"actors":actors,"playwright":playwright,"genre":genre,"country":country})
    print("正在导入csv……")
    data.to_csv("MyMovieData.csv",index=False,sep=',',encoding='utf8')
    print("csv文件生成成功")

