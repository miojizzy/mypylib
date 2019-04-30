#-*- coding:utf-8 -*- 
import time
def NOW():
	return time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())

def listiter(param_vec, num=1):
	tmp_vec = []
	count = 0
	for item in param_vec:
		tmp_vec.append(item)
		count+=1
		if count%num == 0:
			ret = tmp_vec
			tmp_vec = []
			yield ret
	if len(tmp_vec)>0:
		yield tmp_vec

