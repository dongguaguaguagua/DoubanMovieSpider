# -*- coding: utf-8 -*-
from fake_useragent.fake import update
import requests
import json
import random
from bs4 import BeautifulSoup
import sys
import time
from fake_useragent import UserAgent
from update import *


if __name__ == "__main__":
    i=3830
    with open("dic1.json","r") as file:
        data=json.load(file)
    with open("dic2_full.json","r") as file:
        dic2_full=json.load(file)
    proxies = get_qg_proxy()
    ua = UserAgent()
    headers = {'User-Agent': ua.random,'Referer':"https://movie.douban.com",'Cennection':'keep-alive'}
    while(i<164546):
        if(i%40==19):
            proxies = get_qg_proxy()
            time.sleep(60)
            headers = {'User-Agent': ua.random}
            print("更新proxy成功")
        try:
            resp = requests.get("http://www.douban.com/subject/"+str(data[str(i)]), proxies = proxies, headers = headers, timeout=3)
        except:
            print("请求超时，尝试更新proxy")
            time.sleep(3*60)
            proxies = get_qg_proxy()
            headers = {'User-Agent': ua.random}
            print("更新proxy成功")
            continue
        if(resp.status_code != 200):
            if(resp.status_code == 404):
                print("subject=",data[str(i)],"的页面找不到，执行下一个")
                os.system("echo " + str(data[str(i)]) + ": " + dic2_full[str(data[str(i)])] +" >> 404.txt")
                i+=1
                continue
            print("错误码:",resp.status_code,"尝试更新proxy")
            time.sleep(3*60)
            proxies = get_qg_proxy()
            headers = {'User-Agent': ua.random}
            print("更新proxy成功")
            continue

        soup = BeautifulSoup(resp.text, 'lxml')
        if(soup == ""):
            print("soup为空，尝试更新proxy")
            time.sleep(3*60)
            proxies = get_qg_proxy()
            headers = {'User-Agent': ua.random}
            print("更新proxy成功")
            continue
        print("生成第",i,"个电影数据……",resp.status_code)
        dataLine = update_data(soup)
        if(dataLine=="failed"):
            # print(soup)
            print("Failed to extract info")
            continue
        # 生成数据
        os.system("echo \""+str(data[str(i)])+","+dataLine+"\" >> MovieData.csv")
        with open("Data/"+str(data[str(i)])+".json","w") as file:
            file.write(update_json(soup))
        time.sleep(random.random()*3)
        i+=1



