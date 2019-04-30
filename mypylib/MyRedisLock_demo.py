#!/usr/bin/python
# -*- coding:utf-8 -*-

from MyRedisLock import *
############
# demo
############

# 设置redis,并实例化
#MyLockMgr("10.10.160.222")  # 默认为127.0.0.1

# part1
# 简单实现,需要手动加锁和释放 **可能会跳过release导致锁无法释放**
def work1(pa):  
	l = MyLock("qwe")	# 获得一个lock实例,传入key(和超时时间)
	l.Lock()			# 加锁
	print pa
	sleep(1)
	l.Release()			# 释放锁

# part2
# 用with在定义域内加锁，自动释放
def work2(pa):
	with MyLock("qwe") as l: # l为加锁的实例，可以手动释放l.Release()
		print 2
		sleep(1)

# part3
# 使用装饰器给某个函数加锁
def work3(pa):
	lock_func(pa)		# 手动调用函数  **特殊的调用方式会error，如pool.apply_async()调用**
@deco(MyLock("qwe"))	# 给函数加装饰器，实例一个lock
def lock_func(a):
	print a
	sleep(1)

def main():
	work3(0)
	import multiprocessing
	pool = multiprocessing.Pool(processes=2)
	for i in range(6):
		pool.apply_async(func=work3, args=(i,))
	pool.close()
	pool.join()

if __name__ == "__main__":
	main()

