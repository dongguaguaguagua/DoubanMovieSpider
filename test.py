# _*_ coding:utf-8 _*_
# from bs4 import BeautifulSoup
# from update import *

# soup=BeautifulSoup("","lxml")


# with open("example.html","r") as file:
# 	resp=file.read()

# soup = BeautifulSoup(resp,'lxml')

# print(update_data(soup))

# -*- coding: utf-8 -*-
import requests
import json
import random
from bs4 import BeautifulSoup
import sys
import time
from fake_useragent import UserAgent
from update import *

if __name__ == "__main__":
    i=0
    with open("dic1.json","r") as file:
        data=json.load(file)

    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    while(i<2):
        if(i%20==19):
            headers = {'User-Agent': ua.random}
            print("更新ua成功")

        resp = requests.get("http://www.douban.com/subject/35766491", headers = headers)

        if(resp.status_code != 200):
            if(resp.status_code == 404):
                print("subject=",data[str(i)],"的页面找不到，执行下一个")
                i+=1
                continue
            print("错误码 : ",resp.status_code)
            continue

        soup = BeautifulSoup(resp.text, 'lxml')
        if(soup == ""):
            print("soup为空，尝试更新proxy")
            continue
        print("生成第",i,"个电影数据……",resp.status_code)
        dataLine = update_data(soup)
        # 生成数据
        os.system("echo "+str(i)+","+str(data[str(i)])+","+dataLine+" >> MovieData.csv")
        time.sleep(random.random()*3)
        i+=1


