
class Counter():
	def __init__(self,vec=None):
		self._count_dict = {}
		if vec != None:
			for item in vec:
				if item not in self._count_dict:
					self._count_dict[item] = 0
				self._count_dict[item] += 1

	def append(self,item,num=1):
		if item not in self._count_dict:
			self._count_dict[item] = 0
		self._count_dict[item] += num
	def extend(self,vec):
		for item in vec:
			if item not in self._count_dict:
				self._count_dict[item] = 0
			self._count_dict[item] += 1
	def most_common(self,num=1):
		return sorted(self._count_dict.items(), key = lambda x:x[1] ,reverse = True)[:num]
	def get_dict(self):
		return self._count_dict
