import queue
import time, random
from multiprocessing import Queue as q
import queue, time
from multiprocessing import Process as p
from multiprocessing import current_process as currentp
from multiprocessing.managers import BaseManager, BaseProxy
import operator
from multiprocessing import Pool

work = (['A',5],['B',2],['C',1],['D',3])

def work_log(work_data):
    print('process %s waiting %s seconds' % (work_data[0],work_data[1]))
    time.sleep(int(work_data[1]))
    print('process %s finished' % work_data[0])

def pool_handler():
    pool = Pool(4)
    pool.map(work_log,work)

if __name__ == '__main__':
    pool_handler()


