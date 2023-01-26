# -*- coding: utf-8 -*-
import requests
import json
import random
from bs4 import BeautifulSoup
import sys
import pandas
import time
from fake_useragent import UserAgent
from update import *

if __name__ == "__main__":
    i=0
    with open("dic1.json","r") as file:
        data=json.load(file)
    proxies = get_proxy()
    if(proxies == {"status":0}):
        sys.exit(1)
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    while(i<2):
        if(i%20==19):
            proxies = get_proxy()
            headers = {'User-Agent': ua.random}
            print("更新proxy成功")
        try:
            resp = requests.get("http://www.douban.com/subject/"+str(data[str(i)]), proxies = proxies, headers = headers)
        except:
            print("请求超时，尝试更新proxy")
            proxies = get_proxy()
            headers = {'User-Agent': ua.random}
            print("更新proxy成功")
            continue
        if(resp.status_code != 200):
            print("status_code : ",resp.status_code)
            proxies = get_proxy()
            headers = {'User-Agent': ua.random}
            print("更新proxy成功")
            continue

        soup = BeautifulSoup(resp.text, 'lxml')
        if(soup == ""):
            print("soup为空，尝试更新proxy")
            proxies = get_proxy()
            headers = {'User-Agent': ua.random}
            print("更新proxy成功")
            continue
        print("生成第",i,"个电影数据……",resp.status_code)
        update_data(soup)
        time.sleep(random.random()*3)
        i+=1

    data=pandas.DataFrame({"name":name,"post_link":post_link,"year":year,"rating":rating,"rating_people":rating_people,"short_rating_num":short_rating_num,"review_num":review_num,"movie_length":movie_length,"release_date":release_date,"director":director,"actors":actors,"playwright":playwright,"genre":genre,"country":country})
    print("正在导入csv……")
    data.to_csv("MyMovieData.csv",index=False,sep=',',encoding='utf8')
    print("csv文件生成成功")

