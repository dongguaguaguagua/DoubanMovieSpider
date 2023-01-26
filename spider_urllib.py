# -*- coding: utf-8 -*-
import json
import random
from bs4 import BeautifulSoup
import json
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

    if(proxies=={"status":0}):
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

        resp = opener.open("https://www.douban.com/subject/"+str(data[str(i)]))

        soup = BeautifulSoup(resp.read().decode("utf8",'ignore'), 'lxml')
        if(resp.getcode() != 200):
            if(resp.getcode() == 404):
                print("subject=",data[str(i)],"的页面找不到，执行下一个")
                i+=1
                continue
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
        dataLine = update_data(soup)
        os.system("echo "+dataLine+" >> MovieData.csv")
        time.sleep(random.random()*3)
        i+=1



