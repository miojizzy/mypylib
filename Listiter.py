import math
def listiter(param_vec, num=1, mode="line"):
	each_count = num
	if mode == "split":
		each_count = math.ceil(len(param_vec)*1.0 / num)
	if each_count < 1:
		return
	tmp_vec = []
	count = 0
	for item in param_vec:
		tmp_vec.append(item)
		count+=1
		if count%each_count == 0:
			ret = tmp_vec
			tmp_vec = []
			yield ret
	if len(tmp_vec)>0:
		yield tmp_vec

def fileiter(filename, num=1):
	tmp_vec = []
	count = 0
	with open(filename,'r') as f:
		for line in f:
			tmp_vec.append(line.strip())
			count+=1
			if count%num == 0:
				ret = tmp_vec
				tmp_vec = []
				yield ret
	if len(tmp_vec)>0:
		yield tmp_vec

import re
def filedataiter(filename,title):
	tmp_vec = []
	record_flag = 0
	with open(filename,'r') as f:
		for line in f:
			line = line.strip()
#			if line.find( title ) != -1:
			if re.search(title, line ) != None:
				record_flag = 1
				if len(tmp_vec) > 0:
					yield tmp_vec
				tmp_vec = []
				if record_flag == 1:
					tmp_vec.append(line)
			else:
				if record_flag == 1:
					tmp_vec.append(line)
				else:
					continue
	if len(tmp_vec) > 0:
		yield tmp_vec


