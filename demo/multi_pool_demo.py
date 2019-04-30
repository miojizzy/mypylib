#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import multiprocessing
import time
import os


def worker(info):
	pid = os.getpid()# 进程pid
	print "data_idx: %2s  pid:%s  ts:%s"%(str(info) ,os.getpid(), str(time.time())  )
	time.sleep(1)
	return 'return : %s'%(str(info))

def main():
	pool = multiprocessing.Pool(processes = 3, maxtasksperchild = 4)
	for  i in range(20):
		p1 = pool.apply_async(func = worker , args = (i,) )	# 只在进程池满了的时候阻塞
		p2 = pool.apply(func = worker, args = (i,))			# 每一条都会阻塞for 循环  跟单进程一样了
		print p1, p1.get()	# p是子进程的对象，要用p.get()才能得到返回，但是p.get()会产生阻塞
		print p2 			# p就是子进程的返回
	print 'end'
	pool.close()
	pool.join()
	print 'all end'
	pass


if __name__ == '__main__':
	main()




