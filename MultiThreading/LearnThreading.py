import threading


def thread_job():
    print("This is an added Thread, number is %s" % threading.current_thread())


def main():
    added_thread = threading.Thread(target=thread_job)#添加线程
    added_thread.start()#开始线程
    # print(threading.active_count())  # 打印激活的threading
    # print(threading.enumerate())  # 打印所有激活的thread
    # print(threading.current_thread())


if __name__ == '__main__':
    main()
