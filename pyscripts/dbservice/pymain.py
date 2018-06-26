import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/library'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/proto_python'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../dbservice'))

import logger
from defines import *
from framework.DBServer import DBServer

logger = logger.get_logger('pymain')

def init():
	'''初始化python server'''
	print("py init")
	try:
		a = DBServer()
	except Exception as e:
		print("init Exception:",e)


def OnServer(sockfd, type, data):
	print("OnServer:%d,%d,%s"%(sockfd,type,data))
	if type == FD_TYPE_ACCEPT:
		logger.debug('OnServer,type=FD_TYPE_ACCEPT,sock=%s'%sockfd)
		try:
			DBServer().add_rpc_channel(sockfd)
		except Exception as e:
			print("Exception:",e)
	elif type == FD_TYPE_READ:
		logger.debug('OnServer,type=FD_TYPE_READ,sock=%s'%sockfd)
		try:
			DBServer().handle_rpc_channel(sockfd, data)
		except Exception as e:
			print("Exception:",e)
	elif type == FD_TYPE_CLOSE:
		logger.debug('OnServer,type=FD_TYPE_CLOSE,sock=%s'%sockfd)
		try:
			DBServer().del_rpc_channel(sockfd)
		except Exception as e:
			print("Exception:",e)
	elif type == FD_TYPE_TIMER:
		logger.debug('OnServer,type=FD_TYPE_TIMER,sock=%s'%sockfd)
		from common import Timer
		Timer.onTimer(sockfd)  # timerId

	return 1,"success"
