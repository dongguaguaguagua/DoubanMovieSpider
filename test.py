# _*_ coding:utf-8 _*_
from  urllib import request
from fake_useragent import UserAgent
from pandas.core import resample
import requests
import datetime
def get_proxy(choice='http'):
    #芝麻ip时间选优算法
    # 获取芝麻代理ip
    url = "http://webapi.http.zhimacangku.com/getip?num=10&type=2&pro=&city=0&yys=0&port=1&pack=290010&ts=1&ys=0&cs=1&lb=1&sb=0&pb=4&mr=1&regions="
    # url选择json
    body = {}
    headers = {}
    response = requests.post(url, json=body, headers=headers)
    ip_data = response.json()
    if(ip_data['code']==0):
        print("获取ip成功")
        #每次读取10条记录对比，芝麻ip每日免费20个
        global excellent_ip
        global excellent_ip_port
        new_data=ip_data
        member = []
        #建立数据入口
        date1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        d1 = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
        for geshu, val1 in enumerate(ip_data['data']):
            #获得ip个数geshu
            # print(new_data['data'][geshu])
           # 将每个时间转换为时间戳加入新数组
            new_time=new_data['data'][geshu]['expire_time']
            d2 =datetime.datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S')
            d = d2-d1
            sec= format(d.seconds);#获取秒数
            sec=int(sec)
            member.append(sec)

        # 冒泡排序
        member.sort(reverse=True)
        #对比得到该时间的ip
        for geshu2, val2 in enumerate(ip_data['data']):
            #获得ip个数geshu
            new_time2=new_data['data'][geshu2]['expire_time']
            d2 =datetime.datetime.strptime(new_time2, '%Y-%m-%d %H:%M:%S')
            d = d2-d1
            #减去固定的时间点
            sec= format(d.seconds);#获取秒数
            sec=int(sec)
            if(sec==member[0]):
                excellent_ip=new_data['data'][geshu2]['ip']
                excellent_ip_port=new_data['data'][geshu2]['port']

    else:
        print("获取ip失败");

    proxyMeta = "http://%(host)s:%(port)s" % {
        "host" : excellent_ip,
        "port" : excellent_ip_port,
    }
    proxies = {
        "http"  : proxyMeta,
        "https"  : proxyMeta
    }
    print(proxies)
    print("选择ip成功")
    return proxies

ua=UserAgent()
print(ua.random)
# 构建一个Handler处理器对象，参数是一个字典类型，包括代理类型和代理服务器IP+Port
# httpproxy_handler = request.ProxyHandler(get_proxy())
#使用代理
# opener = request.build_opener(httpproxy_handler)
# request = request.Request('https://www.douban.com/subject/35211739/', headers={"User-Agent": ua.random})

#1 如果这么写，只有使用opener.open()方法发送请求才使用自定义的代理，而urlopen()则不使用自定义代理。
# response = opener.open(request)
requestt = request.Request('https://www.douban.com/subject/35211739/', headers={"User-Agent": ua.random})   # 请求处理
response=request.urlopen(requestt)   # 读取结果
#12如果这么写，就是将opener应用到全局，之后所有的，不管是opener.open()还是urlopen() 发送请求，都将使用自定义代理。
#urllib2.install_opener(opener)
#response = urllib2.urlopen(request)

print(response.read().decode("utf-8",'ignore'))
