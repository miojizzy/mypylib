#!/usr/local/python27/bin/python2.7
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import multiprocessing
import time
import os


def read (read_q):
	print '[read] start'
	for i in range(20):
		read_q.put(i)
		print '[read] put task %d , read_q size %d'%(i , read_q.qsize())
		time.sleep(0.3)
	print '[read] end'
				

def write(write_q):
	print "[write] start"
	tm = time.time()
	while True:
		if time.time()-tm > 10:
			break
		if write_q.empty():
			continue
		data = write_q.get()
		print '[write] save',data

def worker(read_q,write_q):
	print '[work pid:%s] start'%(str(os.getpid()) )
	data = read_q.get()
	print '[work pid:%s] deal %d'%(str(os.getpid()), data )
	data = data*10
	write_q.put(data)
	print '[work pid:%s] end'%(str(os.getpid()) )

	
def main():
	manager = multiprocessing.Manager()
	read_q = manager.Queue()
	write_q = manager.Queue()
	p_read = multiprocessing.Process(target = read , args = (read_q,) )
	p_write = multiprocessing.Process(target = write , args = (write_q,) )
	pool = multiprocessing.Pool(processes = 3 , maxtasksperchild = 3)
	pool.apply_async(func = worker , args = (read_q, write_q, ))


	time.sleep(3)
	
	p_write.start()
	p_read.start()
	
	p_read.join()

	while not read_q.empty():
		time.sleep(1)
	pool.close()
	pool.join()

	while not write_q.empty():
		time.sleep(1)
	p_write.join()
	




if __name__ == '__main__':
	main()




