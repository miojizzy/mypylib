

import time
def NOW():
	return time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())

import sys
def LOG(info):
	print NOW(),str(info)
def LOG_SAFE(info):
	print NOW(),str(info)
	sys.stdout.flush()



