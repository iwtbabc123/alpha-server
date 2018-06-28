import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/library'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/proto_python'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../dbservice'))

#import logger
#from defines import *
from framework.DBServer import DBServer
import pymainbase

#logger = logger.get_logger('pymain')

def init():
	'''初始化python server'''
	print("py init")
	try:
		a = DBServer()
	except Exception as e:
		print("init Exception:",e)


def OnServer(sockfd, type, data):
	serverobj = DBServer()
	pymainbase.OnServer(sockfd, type, data, serverobj)
	return 1,"success"
