import urllib.request, urllib.parse


def getHTMLData(baseurl, **kwargs):
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


def baseurlHandler(baseurl):
    urllist =[]
    for i in range(0, 25):  # url 处理
        url = baseurl + str(i * 25)
        urllist.append(url)
    return urllist

if __name__ == '__main__':
    data = bytes(urllib.parse.urlencode({"hello": "world"}), encoding="utf-8")
    dict = {'data': data}
    #getData("http://httpbin.org/post",**dict)
    #getHTMLData("https://www.bilibili.com")
    #print(baseurlHandler("https://movie.douban.com/top250?start="))
    #getHTMLData("http://baidu.com")
    #getHTMLData("https://www.acfun.cn/v/list110/index.htm")
    getHTMLData("https://www.acfun.cn/rest/pc-direct/comment/list?sourceId=15751436&sourceType=3&page=1&pivotCommentId=&newPivotCommentId=&t=1590481192124&supportZtEmot=true")