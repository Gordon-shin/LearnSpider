import urllib.request, urllib.parse
import json
import pymysql
import requests


def getRawData(baseurl, **kwargs):
    headers = {  # 伪装浏览器
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.163 Safari/537.36',
    }
    try:
        request = urllib.request.Request(url=baseurl, headers=headers, data=kwargs.get("data"),method=None)
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
    #print(response)
    return response

def baseurlHandler_Acfun_Article_zonghe(size):
    pageno = 1
    base_url_Acfun_Particle_zonghe = "https://webapi.acfun.cn/query/article/list?pageNo={pageno}&size={size}" \
                 "&realmIds=5%2C22%2C3%2C4&originalOnly=false&orderType=3" \
                 "&periodType=1&filterTitleImage=true".format(pageno=pageno,size=size)
    jsonData =json.loads( getRawData(base_url_Acfun_Particle_zonghe))
    pageno_max = jsonData["data"]["totalPage"]
    articleList = jsonData["data"]["articleList"]
    for aritcle in articleList:
        aritcle["id"]
        aritcle["channel_name"]
        aritcle["title"]
        aritcle["channel_path"]
        aritcle["realm_id"]
        aritcle["status"]
        aritcle["username"]
        aritcle["user_id"]
    print(pageno_max)

def Acfun_Article_zonghe_to_Mysql():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        db='acfun_articles',
        charset='utf8'
    )


def baseurlHandler(baseurl):
    urllist =[]
    for i in range(0, 25):  # url 处理
        url = baseurl + str(i * 25)
        urllist.append(url)
    return urllist

if __name__ == '__main__':
    #data = bytes(urllib.parse.urlencode({"hello": "world"}), encoding="utf-8")
    #dict = {'data': data}
    #getData("http://httpbin.org/post",**dict)
   # baseurlHandler_Acfun_Article_zonghe(50)
    #jsondata = json.loads(getRawData(
    #"https://www.acfun.cn/rest/pc-direct/comment/list?sourceId=15751436&sourceType=3&page=1&pivotCommentId=&newPivotCommentId=&t=1590481192124&supportZtEmot=true"))
    #print(getRawData("https://www.acfun.cn/a/ac15750283"))

    weiboresuo_url = "https://www.enlightent.cn/research/top/getWeiboHotSearchDayAggs.do"
    parameter = {
        "type":"realTimeHotSearchList",
        "t":"1120342775",
        "date":"2020/05/26"
    }
    session = requests.Session()
    response=session.get("https://www.enlightent.cn/research/rank/weiboSearchRank")
    print(session.cookies.get_dict())
    data=bytes(urllib.parse.urlencode(parameter),encoding="utf-8")
    dict = {'data': data}
    rawdata = getRawData(weiboresuo_url,**dict)
    print(rawdata)