# _*_ coding:utf-8 _*_
from  urllib import request
from fake_useragent import UserAgent
from pandas.core import resample
import requests
import datetime
from bs4 import BeautifulSoup
import re
soup=BeautifulSoup("","lxml")
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

# 解析
tmp = re.findall(r"\d+\.?\d*",str(soup.find('span',class_='year')))
if tmp == []:
    year.append("unknown")
else:
    year.append(tmp[0])
# 电影名称
try:
    name.append(soup.findAll(property="v:itemreviewed")[0].text)
except:
    print(soup)
# 海报链接
if(soup.find(rel="v:image")!=None):
    post_link.append(soup.find(rel="v:image").get('src').replace("s_ratio_poster","raw").replace("webp","jpg"))
else:
    post_link.append("None")

# 豆瓣评分
if(soup.findAll(property="v:average")!=[]):
    rating.append(soup.findAll(property="v:average")[0].text)
else:
    rating.append('0')
# 评分个数
if(soup.find('a',class_="rating_people")!=None):
    rating_people.append(re.findall(r"\d+\.?\d*",str(soup.find('a',class_="rating_people")))[0])
else:
    rating_people.append('0')
# 短评数

if(soup.find('div',class_="mod-hd")!=None):
	short_rating_num.append(re.findall(r"\d+\.?\d*",soup.find('div',class_="mod-hd").find_all("a")[1].text)[0])
else:
	short_rating_num.append("0")
# 影评数
if(soup.find(href="reviews")!=None):
	review_num.append(re.findall(r"\d+\.?\d*",soup.find(href="reviews").text)[0])
else:
	review_num.append("0")
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
