import redis
#import uuid
import time
#
# unsafe release, do not check value
#
class MyRedisLockMgr(object):
	def __init__(self, host="127.0.0.1", port=6379, password="", max_connections=5):
		self.pool = redis.ConnectionPool(host=host, port=port, password=password, max_connections=max_connections)

	def Lock(self, key, timeout):
		r = redis.Redis(connection_pool=self.pool)
#		val = str(uuid.uuid4())
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
	
	def Release(self, key):
		r = redis.Redis(connection_pool=self.pool)
		try:
			r.delete(key)
			return True
		except Exception ,e:
			print e
		print "release fail"
		return False
		


def main():
	MyRedisLockMgr = MyRedisLockMgr("10.10.96.117")
	timeout=1
	print 1
	MyRedisLockMgr.Lock("qwer", timeout)
	print 2
	MyRedisLockMgr.Lock("qwer", timeout)
	print 3
	MyRedisLockMgr.Lock("qwer", timeout)
	MyRedisLockMgr.Release("qwer",)
	print 4
	MyRedisLockMgr.Lock("qwer", timeout)
	print 5
	MyRedisLockMgr.Lock("qwer", timeout)
	print 6
	MyRedisLockMgr.Lock("qwer", timeout)
	print 7

if __name__ == "__main__":
	main()






