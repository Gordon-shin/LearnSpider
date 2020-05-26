from bs4 import BeautifulSoup as bs
import re #正则表达式
import urllib.request,urllib.error #定制URL 获取网页数据
import xlwt #进行excel操作
import sqlite3 #数据库操作

#httpbin.org 接口测试网站
def getRawData(baseurl, **kwargs):
    headers = {  # 伪装浏览器
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.163 Safari/537.36'
    }
    try:
        request = urllib.request.Request(url=baseurl, headers=headers, data=kwargs.get("data"))
        response = urllib.request.urlopen(request, timeout=10)
        if response.status == 200:
            response = response.read().decode('utf-8')
        else:
            pass
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    print(response)
    return response


def baseurlHandler(baseurl):# url 处理
    urllist =[]
    for i in range(0, 25):
        url = baseurl + str(i * 25)
        urllist.append(url)
    return urllist

def cleanRawData(rawdata):
    bs(rawdata,"json")
    pass

def getDataList(baseurl):
    datalist=[]
    urllist = getRawData(baseurl)
        #解析数据
    return datalist

def saveData(savePath):
    pass

if __name__ == '__main__':
    #爬取网页
    baseurl="https://movie.douban.com/top250?start="


    print(getRawData(baseurl))
    getDataList(baseurl)
    #解析数据

    #保存数据
    savePath = ".\\豆瓣电影Top250.xls"
    saveData(savePath)