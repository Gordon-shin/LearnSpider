import urllib.request, urllib.parse
import json
import pymysql
import time


class Acfun_Ariticles:

    def getRawData(self, baseurl, **kwargs):
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
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
        # print(response)
        return response

    def Acfun_Article_detail_url_getjsondata(self,url,pageno,size):
        pass

    def baseurlHandler_Acfun_Article_zonghe(self, size):
        pageno = 1
        base_url_Acfun_Particle_zonghe = "https://webapi.acfun.cn/query/article/list?pageNo={pageno}&size={size}" \
                                             "&realmIds=5%2C22%2C3%2C4&originalOnly=false&orderType=3&" \
                                             "periodType=-1&filterTitleImage=true".format(pageno=str(pageno), size=str(size))
        jsonData = json.loads(self.getRawData(base_url_Acfun_Particle_zonghe))
        pageno_max = jsonData["data"]["totalPage"]

        for pageno  in range(1,int(pageno_max)):
            print("第"+str(pageno)+"次入库")
            base_url_Acfun_Particle_zonghe = "https://webapi.acfun.cn/query/article/list?pageNo={pageno}&size={size}" \
                                             "&realmIds=5%2C22%2C3%2C4&originalOnly=false&orderType=3&" \
                                             "periodType=-1&filterTitleImage=true".format(pageno=str(pageno), size=str(size))
            jsonData = json.loads(self.getRawData(base_url_Acfun_Particle_zonghe))
            articleList = jsonData["data"]["articleList"]
            values = []
            for aritcle in articleList:
                values.append((
                    aritcle["id"],
                    aritcle["channel_name"],
                    aritcle["title"],
                    aritcle["channel_path"],
                    aritcle["realm_id"],
                    aritcle["status"],
                    aritcle["username"],
                    aritcle["user_id"],
                    aritcle["comment_count"],
                    aritcle["banana_count"],
                    aritcle["favorite_count"],
                    aritcle["recommended"],
                    aritcle["view_count"],
                    aritcle["contribute_time"],
                    aritcle["latest_active_time"],
                    aritcle["latest_comment_time"],
                ))
            self.Acfun_Article_detail_to_Mysql_Insert(values)
            print(pageno_max)
           # print(values)

    def pymysql_config(self):
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            db='acfun_articles',
            charset='utf8mb4'
        )
        return conn

    def Acfun_Article_detail_to_Mysql_Insert(self, values):
        conn = self.pymysql_config()
        try:
            # 获取游标
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            # 执行sql语句
            sql = "INSERT INTO articles_detail VALUES" \
                  "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            rows = cursor.executemany(sql,values)
            if rows>0:
                print("入库成功"+str(rows))
                conn.commit()
                cursor.close()
                conn.close()
            else:
                print("入库失败")
                cursor.close()
                conn.close()
        except Exception as e:
            print(e)

    def baseurlHandler(self, baseurl):
        urllist = []
        for i in range(0, 25):  # url 处理
            url = baseurl + str(i * 25)
            urllist.append(url)
        return urllist

    def __init__(self):
        #self.Acfun_Article_zonghe_to_Mysql_Insert()
       # data = bytes(urllib.parse.urlencode({"hello": "world"}), encoding="utf-8")
        #dict = {'data': data}
        # getData("http://httpbin.org/post",**dict)
        self.baseurlHandler_Acfun_Article_zonghe(10)
        # jsondata = json.loads(getRawData(
        # "https://www.acfun.cn/rest/pc-direct/comment/list?sourceId=15751436&sourceType=3&page=1&pivotCommentId=&newPivotCommentId=&t=1590481192124&supportZtEmot=true"))
        # print(getRawData("https://www.acfun.cn/a/ac15750283"))


if __name__ == '__main__':
    Acfun_Ariticles = Acfun_Ariticles()
