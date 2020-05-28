import threading
import time
from queue import Queue


def job(list,queue):
    for i in range(len(list)):
        list[i] = list[i] ** 2;
    queue.put(list)


def multithreading():
    q = Queue()
    threads = []
    data = [[1, 2, 3], [3, 4, 5], [4, 4, 4], [5, 5, 5]]
    for i in range(4):
        t = threading.Thread(target=job, args=(data[i], q))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    result=[]
    for _ in range(4):
        result.append(q.get())
    print(result)

if __name__ == '__main__':
    multithreading()