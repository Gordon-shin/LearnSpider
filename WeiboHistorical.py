import json

import pymysql
import requests


def requests_web_data(url):
    try:
        headers = {"User-Agent": "", "Cookie": ""}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        print('requests error!')
    else:
        return r.content

def get_weibo_historical_data(min):
    latest_time_id_url = 'https://www.eecso.com/test/weibo/apis/getlatest.php'
    latest_time_id = json.loads(requests_web_data(latest_time_id_url).decode('utf-8'))
    # 筛选获取time_id
    time_ids = []
    #for x in range(241, int(latest_time_id) + 1, 360):    # time_id=48438：2020-01-01
    #for x in range(241, int(latest_time_id) + 1, 90):    # time_id=48438：2020-01-01
    for x in range(241, int(latest_time_id[0]) + 1, int(min/2)):    # time_id=48438：2020-01-01
        time_id_url = 'https://www.eecso.com/test/weibo/apis/getlatest.php?timeid=' + str(x)
        time_data = json.loads(requests_web_data(time_id_url).decode('utf-8'))
        # print("当前处理" + str(x))
        # time_ids.append(x)
        if time_data is not None:
           # time = time_data[1].split(' ')[1].split(':')[0]  # ['48798', '2020-01-01 12:00:01']
           # if time == '00' or time == '12':
            print("当前处理" + str(time_data))
            time_ids.append(time_data)
            #print(time_ids)
        # time_ids.append(time_data[0])
    if time_ids[-1][0] != latest_time_id[0]:
        time_ids.append(latest_time_id)
    return time_ids


def get_weibo_hot_data(time_ids):
    weibo_hot_data = []
    for time_id in time_ids:
        historical_data_url = 'https://www.eecso.com/test/weibo/apis/currentitems.php?timeid=' + str(time_id[0])
        data = json.loads(requests_web_data(historical_data_url).decode('utf-8'))
        print("当前处理" + str(time_id[0])+"  共"+str(len(data)))
        for item in data:
            item.append(time_id[0])
            item.append(time_id[1])
        weibo_hot_data.append(data)
    return weibo_hot_data

def pymysql_config():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        db='weibo_hot_data',
        charset='utf8mb4'
    )
    return conn

def weibo_hot_data_insert(conn,weibohotdata):
    try:
        # 获取游标
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 执行sql语句
       # sql = "INSERT INTO weibo_hot_everyday VALUES" \
       # sql = "INSERT INTO weibo_hot_everyday_three_hours(title,last_appear_time,start_appear_time,hit_nums,timeid) VALUES" \
        sql = "INSERT INTO weibo_hot_everyday_one_hour(title,last_appear_time,start_appear_time,hit_nums,timeid,accurate_time) VALUES" \
              "(%s,%s,%s,%s,%s,%s) "
        rows = cursor.executemany(sql, weibohotdata)
        if rows > 0:
            print("入库成功" + str(rows))
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("入库失败")
            cursor.close()
            conn.close()
    except Exception as e:
        print(e)

def main():
    time_ids =get_weibo_historical_data(60)
    #time_ids = [['241', '2019-10-26 00:30:01'], ['90241', '2020-02-28 01:34:02'], ['155424', '2020-05-28 14:48:01']]
    #time_ids = [241,601]
    weibo_hot_data_list = get_weibo_hot_data(time_ids=time_ids)
    '''if(len(time_ids)==len(weibo_hot_data_list)):
        print("数据全部获取成功")
    else:
        print("time_ids:"+str(len(time_ids)))
        print("weibo_hot_data_list:"+len(weibo_hot_data_list))
    '''

    for daydata in weibo_hot_data_list:
        conn = pymysql_config()
        weibo_hot_data_insert(conn, daydata)

main()
#print(get_weibo_historical_data(180000))
#print(requests_web_data("https://s.weibo.com/top/summary").decode('utf-8'))