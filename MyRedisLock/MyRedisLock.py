#!/usr/bin/python27
# -*- coding:utf-8 -*-
import redis
import time
import uuid
import sys
sys.path.append("../Singleton")
from Singleton import singleton



# part 0
@singleton
class MyLockMgr(object):
	def __init__(self, host="127.0.0.1", port=6379, password="", max_connections=5):
		try:
			self.pool = redis.ConnectionPool(host=host, port=port, password=password, max_connections=max_connections)
		except Exception ,e:
			print "[ERROR]connect to redis error !",e



class MyLock(object):
	def __init__(self, key="default_key", timeout=600):
		self.mgr = MyLockMgr()
		self.key = key
		self.val = str(uuid.uuid4())
		self.timeout = timeout
		pass
	
# part 0 
# **不使用**
# 对于某key的加锁及释放， 不检查val，可能会被非法释放
	def _Lock(self, key, timeout):
		r = redis.Redis(connection_pool=self.pool)
		val = "1"
		try:
			while True:
				if r.setnx(key, val):
					r.expire(key, timeout)
					return True
				time.sleep(0.01)
		except Exception ,e:
			print e
		print "lock fail"
		return False
	def _Release(self, key):
		r = redis.Redis(connection_pool=self.pool)
		try:
			r.delete(key)
			return True
		except Exception ,e:
			print e
		print "release fail"
		return False

# part 1
	def Lock(self):
		r = redis.Redis(connection_pool=self.mgr.pool)
		try:
			while True:
				if r.setnx(self.key, self.val):  # 存在key则false不存在则set成功，atom操作
					r.expire(self.key, self.timeout)  # 设定超时时间
					return True
				time.sleep(0.01)
		except Exception ,e:
			print e
		print "lock fail"
		return False
	def Release(self):
		r = redis.Redis(connection_pool=self.mgr.pool)
		pipe = r.pipeline(True)  # pipeline保证atom
		try:
			pipe.watch(self.key)  # 监视key
			if pipe.get(self.key) == self.val:
				pipe.multi()  # 事务开始
				pipe.delete(self.key) 
				pipe.execute() # 事务提交
			pipe.unwatch() # 监视结束，如果期间被其他修改则raise
			return True
		except Exception ,e:
			print e
		print "release fail"
		return False

# part 2
	def __enter__(self):
		self.Lock()
		return self  # 返回lock实例本身
	def __exit__(self,  exc_type, exc_val, exc_tb):
		return self.Release()

# part 3
def deco(cls):
	def _deco(func):
		def __deco(*args, **kwargs):
			with cls as l:
				try:
					return func(*args, **kwargs)
				except Exception ,e:
					print e
		return __deco
	return _deco




############
# demo
############

# 设置redis,并实例化
#MyLockMgr("10.10.160.222")

# part1
# 简单实现,需要手动加锁和释放 **可能会跳过release导致锁无法释放**
def work1(pa):  
	l = MyLock("qwe")	# 获得一个lock实例,传入key(和超时时间)
	l.Lock()			# 加锁
	print pa
	time.sleep(1)
	l.Release()			# 释放锁

# part2
# 用with在定义域内加锁，自动释放
def work2(pa):
	with MyLock("qwe") as l: # l为加锁的实例，可以手动释放l.Release()
		print 2
		time.sleep(1)

# part3
# 使用装饰器给某个函数加锁
def work3(pa):
	lock_func(pa)		# 手动调用函数  **特殊的调用方式会error，如pool.apply_async()调用**
@deco(MyLock("qwe"))	# 给函数加装饰器，实例一个lock
def lock_func(a):
	print a
	time.sleep(1)

def main():
	work3(0)
	sys.exit()
	import multiprocessing
	pool = multiprocessing.Pool(processes=2)
	for i in range(6):
		pool.apply_async(func=work3, args=(i,))
	pool.close()
	pool.join()

if __name__ == "__main__":
	main()

