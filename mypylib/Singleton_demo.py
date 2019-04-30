#!/usr/bin/python
# -*- coding-utf8 -*-

print "py start"
import Singleton
print "import end"

print "class A define start"
@Singleton.singleton
class A(object):
	def __init__(self, num):
		print "A.__init__ start"
		self.num = num
		print "A.__init__ end"
print "class A define end"

print "class B define start"
@Singleton.singleton
class B(object):
	def __init__(self, num):
		print "B.__init__ start"
		self.num = num
		print "B.__init__ end"
print "class B define end"

def main():
	print "main start"
	a = A(1)
	b = A(2)
	print a.num
	print b.num
	c = B(3)
	d = B(4)
	print c.num
	print d.num


if __name__ == "__main__":
	main()
