# _*_ coding:utf-8 _*_
from  urllib import request
from fake_useragent import UserAgent
from pandas.core import resample
import requests
import datetime
from bs4 import BeautifulSoup
from update import *

soup=BeautifulSoup("","lxml")


with open("example.html","r") as file:
	resp=file.read()

soup = BeautifulSoup(resp,'lxml')
update_data(soup)


print("上映年份:",year)
print("电影名称:",name)
print("海报链接:",post_link)
print("豆瓣评分:",rating)
print("评分个数:",rating_people)
print("短评数:",short_rating_num)
print("影评数:",review_num)
print("电影时长:",movie_length)
print("上映日期:",release_date)
print("导演:",director)
print("编剧:",playwright)
print("演员:",actors)
print("体裁:",genre)
print("国家:",country)
