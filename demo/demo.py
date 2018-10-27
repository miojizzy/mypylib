#!/usr/bin/python
#!/usr/local/python27/bin/python2.7
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import multiprocessing
import time
import os

#import MultiTqdm



import tqdm

def work(idx, desc):
	pbar = tqdm.tqdm(total=100, position=idx+1, desc=desc)
	for i in range(100):
		time.sleep(0.02)
		pbar.update()

count=0
p_vec = [ multiprocessing.Process(target=work, args = (i, count ))  for i in range(3) ]




for p in p_vec:
	p.start()
	time.sleep(0.2)
for p in p_vec:
	p.join()

print ""





#if __name__ == '__main__':
#	main()




