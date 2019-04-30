class singleton(object):
	def __init__(self, cls):
		self._cls = cls
		self._instances = None
	def __call__(self,*args):
		if not self._instances:
			self._instances = self._cls(*args)
		return self._instances






