#!/usr/bin/python273
import logging

_log_file = "log"
_format_str = '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s'



logging.basicConfig(level=logging.DEBUG
		,format=_format_str
		,datefmt='%Y-%m-%d %H:%M:%S'
#		,filename='myapp.log'
#		,filemode='w'
)
######## make log file
from logging.handlers import RotatingFileHandler
Rthandler = RotatingFileHandler(_log_file , maxBytes=100*1024*1024,backupCount=5)
Rthandler.setLevel(logging.DEBUG)
formatter = logging.Formatter(_format_str)
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)


