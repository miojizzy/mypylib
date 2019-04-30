# -*- coding:utf-8 -*-
from time import sleep
from uuid import uuid4
from redis import ConnectionPool, Redis
from Singleton import singleton
# part 0
@singleton
class MyLockMgr(object):
	def __init__(self, host="127.0.0.1", port=6379, password="", max_connections=5):
		try:
			self.pool = ConnectionPool(host=host, port=port, password=password, max_connections=max_connections)
		except Exception ,e:
			print "[ERROR]connect to redis error !",e



class MyLock(object):
	def __init__(self, key="default_key", timeout=600):
		self.mgr = MyLockMgr()
		self.key = key
		self.val = str(uuid4())
		self.timeout = timeout
		pass
	
# part 0 
# **不使用**
# 对于某key的加锁及释放， 不检查val，可能会被非法释放
	def _Lock(self, key, timeout):
		r = Redis(connection_pool=self.pool)
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
		r = Redis(connection_pool=self.pool)
		try:
			r.delete(key)
			return True
		except Exception ,e:
			print e
		print "release fail"
		return False

# part 1
	def Lock(self):
		r = Redis(connection_pool=self.mgr.pool)
		try:
			while True:
				if r.setnx(self.key, self.val):  # 存在key则false不存在则set成功，atom操作
					r.expire(self.key, self.timeout)  # 设定超时时间
					return True
				sleep(0.01)
		except Exception ,e:
			print e
		print "lock fail"
		return False
	def Release(self):
		r = Redis(connection_pool=self.mgr.pool)
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




