import json
# import pandas
import os
from bs4 import BeautifulSoup, NavigableString, Comment
import requests
import re
# data=pandas.read_csv("/Users/huzongyu/大学/数据世界探秘/moviedata/Data/movies.csv",encoding='utf8',usecols=['MOVIE_ID','NAME'])
# dic={}
# j=0
# for i in data['MOVIE_ID']:
# 	dic[i]=data['NAME'][j]
# 	j+=1

# file=[]
# # 读取文件名
# for filename in os.walk("/Users/huzongyu/大学/数据世界探秘/moviedata/MovieJSON/data/"):
# 	file=filename[2]

# # 判断是否存在重复
# count=0
# dic2={}
# for i in file:
# 	if(int(i.replace(".json","")) in dic):
# 		continue
# 	else:
# 		with open("/Users/huzongyu/大学/数据世界探秘/moviedata/MovieJSON/data/"+i,"r") as file:
# 			j=file.read()
# 		j=json.loads(j)
# 		dic[i.replace(".json","")]=j['title']

# print(dic)

# data=pandas.read_csv("/Users/huzongyu/大学/数据世界探秘/moviedata/Data/movies.csv",encoding='utf8',usecols=['MOVIE_ID','NAME'])
# dic=[]
# j=0
# for i in data['MOVIE_ID']:
# 	dic.append(data['MOVIE_ID'][j])
# 	j+=1

# file=[]
# # 读取文件名
# for filename in os.walk("/Users/huzongyu/大学/数据世界探秘/moviedata/MovieJSON/data/"):
# 	file=filename[2]

# # 判断是否存在重复
# count=0

# for i in file:
# 	if(int(i.replace(".json","")) in dic):
# 		continue
# 	else:
# 		dic.append(int(i.replace(".json","")))

# print(dic)
a=[]
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

with open("example.html","r") as file:
	resp=file.read()
with open("dic1.json","r") as file:
	data=json.load(file)

headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",}

soup = BeautifulSoup(resp,'lxml')

# 解析
# 上映日期
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


# j=json.loads(j)
# print(sorted(j.items(),key=lambda kv:(kv[1], kv[0])))
# print(d.replace("\": \"","π").replace("\",\n\"","®"))
# print(d.replace("π","\": \"").replace("®","\",\n\""))

# print((25828589 in ))

