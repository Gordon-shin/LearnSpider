import urllib

import requests


def weibo_rank_spider():
    session = requests.Session()
    weiboresuo_url = "https://www.enlightent.cn/research/top/getWeiboHotSearchDayAggs.do"
    parameter = {
        'type': 'realTimeHotSearchList',
        't': '1120342775',
        'date': '2019/05/27'
    }
    source_code = session.post(weiboresuo_url, params=parameter)
    print(source_code)
def get_raw_data(url, **kwargs):

    try:
        request = urllib.request.Request(url=url, headers=kwargs.get("headers"), data=kwargs.get("data"),
                                         method=kwargs.get("method"))
        response = urllib.request.urlopen(request, timeout=10)
        if response.status == 200:
            response = response.read().decode('utf-8')
        else:
            pass
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    # print(response)
    return response

if __name__ == '__main__':

    weiboresuo_url = "https://www.enlightent.cn/research/top/getWeiboHotSearchDayAggs.do"
    parameter = {
        'type': 'realTimeHotSearchList',
        't': '1120342775',
        'accessToken':'',
        'date': '2020/05/24'
    }
    headers = {  # 伪装浏览器
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.163 Safari/537.36',
    }
    weiboresuo_url_index = "https://www.enlightent.cn/research/rank/weiboSearchRank"
    #parameter = bytes(urllib.parse.urlencode(parameter), encoding="utf-8")
    requests_session = requests.session()

    response = requests.post(url=weiboresuo_url,data=parameter,headers=headers)
    print(response.content.decode('utf-8'))
