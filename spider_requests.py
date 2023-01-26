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

        resp = requests.get("http://www.douban.com/subject/"+str(data[str(i)]), proxies = proxies, headers = headers)

        if(resp.status_code != 200):
            if(resp.status_code == 404):
                print("subject=",data[str(i)],"的页面找不到，执行下一个")
                i+=1
                continue
            print("错误码 : ",resp.status_code,"尝试更新proxy")
            time.sleep(3)
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
        dataLine = update_data(soup)
        os.system("echo "+dataLine+" >> MovieData.csv")
        time.sleep(random.random()*3)
        i+=1


