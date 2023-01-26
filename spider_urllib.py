# -*- coding: utf-8 -*-
import requests
import json
import random
import datetime
from bs4 import BeautifulSoup
import re
import pandas
import time
import sys
from fake_useragent import UserAgent
import urllib.request
from update import *


if __name__ == "__main__":
    i=0
    with open("dic1.json","r") as file:
        data=json.load(file)

    ua=UserAgent()

    headers = [('User-Agent', ua.random),('Referer',"https://movie.douban.com"),('Cennection','keep-alive')]

    proxies = get_proxy()
    if(proxies == "获取ip失败"):
        sys.exit(1)

    # 传递proxy
    proxy_handler = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(proxy_handler)
    # 设置请求头
    opener.addheaders = headers

    while(i<100):
        if(i%20==19):
            # 更新proxy
            proxies = get_proxy()
            # 传递proxy
            proxy_handler = urllib.request.ProxyHandler(proxies)
            opener = urllib.request.build_opener(proxy_handler)
            # 设置请求头
            opener.addheaders = headers
            print("更新proxy完成")

        try:
            resp = opener.open("https://www.douban.com/subject/"+str(data[str(i)]))
        except:
            print("请求超时，尝试更新proxy")
            # 更新proxy
            proxies = get_proxy()
            # 传递proxy
            proxy_handler = urllib.request.ProxyHandler(proxies)
            opener = urllib.request.build_opener(proxy_handler)
            # 设置请求头
            opener.addheaders = headers
            print("更新proxy完成")
            continue
        soup = BeautifulSoup(resp.read().decode("utf8",'ignore'), 'lxml')
        if(resp.getcode() != 200):
            print("status_code : ",resp.status_code)
            # 更新proxy
            proxies = get_proxy()
            # 传递proxy
            proxy_handler = urllib.request.ProxyHandler(proxies)
            opener = urllib.request.build_opener(proxy_handler)
            # 设置请求头
            opener.addheaders = headers
            print("更新proxy完成")
            continue
        elif(soup == ""):
            print("soup为空，尝试更新proxy")
            # 更新proxy
            proxies = get_proxy()
            # 传递proxy
            proxy_handler = urllib.request.ProxyHandler(proxies)
            opener = urllib.request.build_opener(proxy_handler)
            # 设置请求头
            opener.addheaders = headers
            print("更新proxy完成")
            continue
        print("生成第",i,"个电影数据……",resp.getcode())
        update_data(soup)
        time.sleep(random.random()*3)
        i+=1

    data=pandas.DataFrame({"name":name,"post_link":post_link,"year":year,"rating":rating,"rating_people":rating_people,"short_rating_num":short_rating_num,"review_num":review_num,"movie_length":movie_length,"release_date":release_date,"director":director,"actors":actors,"playwright":playwright,"genre":genre,"country":country})
    print("正在导入csv……")
    data.to_csv("MyMovieData.csv",index=False,sep=',',encoding='utf8')
    print("csv文件生成成功")

