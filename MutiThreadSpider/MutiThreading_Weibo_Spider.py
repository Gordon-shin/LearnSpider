import json
import pymysql
import requests
from queue import Queue
import threading

'''
Queue.qsize(队列名) #返回队列的大小
Queue.empty(队列名) # 队列为空返回true，否则为false
Queue.full(队列名) # 队列满返回true
Queue.get(队列名,值) # 出队
Queue.put(队列名,值) # 入队
FIFO 先进先出
'''

'''
公共变量和方法
'''


def get_threads_name_list(listname, threadsnum):
    list = []
    for i in range(0, int(threadsnum)):
        list.append(str(listname) + str(i))
    return list


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


class Crawl_Timeids_thread(threading.Thread):
    def __init__(self, thread_id, timeids_queue):  # queue 爬取timeid详细信息的队列
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.timeids_queue = timeids_queue

    def run(self):
        '''
        线程在调用过程中就会调用对应的run方法
        :return:
        '''
        print('启动线程：', self.thread_id)
        self.crawl_spider()
        print('退出了该线程：', self.thread_id)

    def crawl_spider(self):
        while True:
            if self.timeids_queue.empty():
                break
            else:
                time_id = self.timeids_queue.get()
                print('[thread_id:', self.thread_id, '][', 'timeid:', time_id, ']')
                time_id_url = 'https://www.eecso.com/test/weibo/apis/getlatest.php?timeid=' + str(time_id)
                try:
                    time_data = json.loads(requests_web_data(time_id_url).decode('utf-8'))
                    if time_data is not None:
                        TIME_DETAIL_DATA_QUEUE.put(time_data)
                except Exception as e:
                    print('获取时间数据进程错误,进程名为', self.getName(), '错误为：', e)


class Crawl_ResouDetail_thread(threading.Thread):
    def __init__(self, thread_id, time_ids):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = time_ids
        self.flag = False
        self.num = RESOU_NUM

    def run(self):
        '''
        线程在调用过程中就会调用对应的run方法
        :return:
        '''
        print('启动线程：', self.thread_id)
        while not self.flag:
            try:
                time_id = self.queue.get(False)  # 若队列为空本行会抛出错误
                if not time_id:
                    pass
                self.crawl_spider(time_id)
                self.queue.task_done()
            except Exception as e:
                pass
        print('退出了该线程：', self.thread_id)

    def crawl_spider(self, time_id):
        # while True:
        # if self.queue.empty():
        #     break
        # else:
        # time_id = self.queue.get()
        print('[thread_id:', self.thread_id, '][', 'timeid:', time_id[0], ']')
        historical_data_url = 'https://www.eecso.com/test/weibo/apis/currentitems.php?timeid=' + str(time_id[0])
        try:
            data = json.loads(requests_web_data(historical_data_url).decode('utf-8'))
            if data is not None:
                for item in data:
                    item.append(time_id[0])
                    item.append(time_id[1])
                    self.num.put("123")
            RESOU_DETAIL_DATA_QUEUE.put(data)

        except Exception as e:
            print('获取时间数据进程错误,进程名为', self.getName(), '错误为：', e)


class Mysql_insert_thread(threading.Thread):
    def __init__(self, thread_id, resou_detail_data):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = resou_detail_data
        self.flag = False
        self.num = MYSQL_INSERT_NUM

    def pymysql_config(self):
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            db='weibo_hot_data',
            charset='utf8mb4'
        )
        return conn

    def run(self):
        '''
        线程在调用过程中就会调用对应的run方法
        :return:
        '''
        print('启动线程：', self.thread_id)
        while not self.flag:
            try:
                onedaydata = self.queue.get(False)  # 若队列为空本行会抛出错误
                if not onedaydata:
                    pass
                conn = self.pymysql_config()
                self.insert(onedaydata, conn)
                self.queue.task_done()
            except Exception as e:
                pass
        print('退出了该线程：', self.thread_id)

    def insert(self, onedaydata, conn):
        print('[thread_id:', self.thread_id, '][', 'timeid:', onedaydata[0][1], ']')

        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = "INSERT INTO weibo_hot_everyday_one_hour(title,last_appear_time,start_appear_time,hit_nums,timeid,accurate_time) VALUES" \
                  "(%s,%s,%s,%s,%s,%s) "
            rows = cursor.executemany(sql, onedaydata)
            if rows > 0:
                print("入库成功" + str(rows))
                conn.commit()
                cursor.close()
                conn.close()
                for i in range(0,rows) :
                    self.num.put("123")
            else:
                print("入库失败")
                cursor.close()
                conn.close()
        except Exception as e:
            print('入库错误,进程名为', self.getName(), '错误为：', e)


'''
    主函数
'''

TIME_DETAIL_DATA_QUEUE = Queue();
flag = False
RESOU_DETAIL_DATA_QUEUE = Queue();
RESOU_NUM = Queue()
MYSQL_INSERT_NUM = Queue()


def main(threadsnum, min):  # 线程数,热搜间隔60为一个小时
    timeids_queue = Queue()  # 初始化timeid队列
    latest_time_id_url = 'https://www.eecso.com/test/weibo/apis/getlatest.php'
    latest_time_id = json.loads(requests_web_data(latest_time_id_url).decode('utf-8'))
    for x in range(241, int(latest_time_id[0]) + 1, int(min / 2)):
        timeids_queue.put(x)  # 构造timeid 队列
    # 初始化时间数据采集线程 （流水线1）
    print('共要爬的数据', timeids_queue.qsize())
    Crawl_Timeids_threads = []  # 存放时间详细线程列表
    Crawl_Timeids_threads_name_list = get_threads_name_list('Crawl_Timeids', threadsnum)
    for thread_id in Crawl_Timeids_threads_name_list:
        thread = Crawl_Timeids_thread(thread_id, timeids_queue)
        thread.start()
        Crawl_Timeids_threads.append(thread)
    # 初始化热搜数据数据采集线程 （流水线2）
    Crawl_ResouDetail_threads = []
    Crawl_ResouDetail_thread_name_list = get_threads_name_list('Crawl_ResouDetail', threadsnum)
    for ResouDetail in Crawl_ResouDetail_thread_name_list:
        thread = Crawl_ResouDetail_thread(ResouDetail, TIME_DETAIL_DATA_QUEUE)
        thread.start()
        Crawl_ResouDetail_threads.append(thread)
    # 初始化数据入库线程 （流水线3）:
    Mysql_insert_threads = []
    Mysql_insert_thread_name_list = get_threads_name_list('Mysql_insert', threadsnum)
    for Mysql_insert in Mysql_insert_thread_name_list:
        thread = Mysql_insert_thread(Mysql_insert, RESOU_DETAIL_DATA_QUEUE)
        thread.start()
        Mysql_insert_threads.append(thread)
    while not timeids_queue.empty():  # 流水线1队列中有数据就阻塞
        pass
    for t in Crawl_Timeids_threads:
        t.join()
    # print('获得的时间详细数据', TIME_DETAIL_DATA_QUEUE.qsize())

    while not TIME_DETAIL_DATA_QUEUE.empty():
        pass

    for t in Crawl_ResouDetail_threads:
        t.flag = True
        t.join()
    # print('获得的热搜详细数据', RESOU_DETAIL_DATA_QUEUE.qsize())
    while not RESOU_DETAIL_DATA_QUEUE.empty():
        pass

    for t in Mysql_insert_threads:
        t.flag = True
        t.join()
    print('爬虫爬到有',RESOU_NUM.qsize(),'条热搜数据')
    print('MYsql成功入库', MYSQL_INSERT_NUM.qsize(), '条热搜数据')

if __name__ == '__main__':
    main(12, 60)
