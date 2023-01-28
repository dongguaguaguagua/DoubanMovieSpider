# _*_ coding:utf-8 _*_
# from bs4 import BeautifulSoup
# from update import *

# soup=BeautifulSoup("","lxml")


# with open("example.html","r") as file:
# 	resp=file.read()

# soup = BeautifulSoup(resp,'lxml')

# print(update_data(soup))

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

# cookies = {
#     '_pk_ref.100001.8cb4': '%5B%22%22%2C%22%22%2C1674730953%2C%22https%3A%2F%2Fmovie.douban.com%2Fsubject%2F26909530%2Fcomments%3Fsort%3Dfollows%22%5D',
#     '_pk_id.100001.8cb4': '39611eaf77a5f71a.1590926023.74.1674730953.1674727089.',
#     '__utma': '30149280.1349727348.1590926023.1674730967.1674734184.153',
#     '__utmz': '30149280.1674730967.152.103.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
#     '__utmv': '30149280.21854',
#     'douban-profile-remind': '1',
#     'gr_user_id': 'fc4d2291-5e05-483b-b2f7-4a3f7d1d36a9',
#     'viewed': '"36085236_10518092_2013619_35467797_10864156_19970064_1882895_1873231_4825444_35269186"',
#     'douban-fav-remind': '1',
#     '_ga_RXNMP372GL': 'GS1.1.1659168343.3.0.1659168344.59',
#     '_ga': 'GA1.1.79818507.1639224921',
#     'Hm_lvt_19fc7b106453f97b6a84d64302f21a04': '1651805621',
#     '__gads': 'ID=8c19a0124d0eeb3c-226dfb8923d300bf:T=1652279314:RT=1652279314:S=ALNI_MaegXjai46UNKGT8tfVw_dAttCMuA',
#     '__gpi': 'UID=0000058b2491022c:T=1652888389:RT=1659257762:S=ALNI_Ma4e4kXXOjgcPzYgvRTIZvAB1sZ5A',
#     '__yadk_uid': 'osOplxYpmtovOEBdxZxN4qs6AcvE6Ndw',
#     'bid': 'QiNBKoE0WC4',
#     'll': '"108296"',
#     'ct': 'y',
#     'dbcl2': '"218545496:FcPWCtQm8Ss"',
#     'push_noty_num': '0',
#     'push_doumail_num': '0',
#     'ck': 'QnGD',
#     'frodotk_db': '"e3a5e9cbd6b6a463aaf1bd638423ed29"',
#     '__utmc': '30149280',
#     '__utmb': '30149280.0.10.1674734184',
# }

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0',
#     'Accept': '*/*',
#     'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#     'Referer': 'https://movie.douban.com/subject/1291543/',
#     'Connection': 'keep-alive',
#     'Sec-Fetch-Dest': 'script',
#     'Sec-Fetch-Mode': 'no-cors',
#     'Sec-Fetch-Site': 'same-site',
# }

# params = {
#     'callback': 'jsonp_11b3nksw888zuk4',
# }

# if __name__ == "__main__":
#     i=0
#     with open("dic1.json","r") as file:
#         data=json.load(file)

#     ua = UserAgent()

#     while(i<2000):
#         resp = requests.get("http://www.douban.com/subject/27148159", params=params, cookies=cookies, headers = headers)

#         if(resp.status_code != 200):
#             if(resp.status_code == 404):
#                 print("subject=",data[str(i)],"的页面找不到，执行下一个")
#                 i+=1
#                 continue
#             print("错误码 : ",resp.status_code)
#             continue

#         soup = BeautifulSoup(resp.text, 'lxml')
#         if(soup == ""):
#             print("soup为空，尝试更新proxy")
#             continue
#         print("生成第",i,"个电影数据……",resp.status_code)
#         dataLine = update_data(soup)

#         # 生成数据
#         os.system("echo \""+str(i)+","+str(data[str(i)])+","+dataLine+"\" >> MovieData.csv")

#         i+=1

with open("example.html","r") as html:
    data=html.read()

soup=BeautifulSoup(data,"lxml")

print(update_data(soup))

# proxxxy=get_qg_proxy()
# headers = {'User-Agent': UserAgent().random}
# resp=requests.get("http://httpbin.org/get",headers=headers,proxies=proxxxy)
# print(resp)

# a={'Code': 0, 'Data': [{'IP': '180.121.132.37', 'port': '21504', 'deadline': '2023-01-26 21:30:20', 'host': '180.121.132.37:21504'}], 'Num': 1, 'TaskID': '8kZYWw0ScIxqxF2j'}
# print(a['Data'][0]['port'])
