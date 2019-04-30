from distutils.core import setup

setup(name='mypylib', version='1.0', author='zzy',
		py_modules=[
			'mypylib.Function',
			'mypylib.Singleton',
			'mypylib.MyRedisLock',
			])
