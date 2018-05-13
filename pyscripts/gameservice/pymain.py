import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/library'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/proto_python'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../gameservice'))

import logger
from defines import *
from GameServer import GameServer

logger = logger.get_logger('pymain')

def init():
	'''初始化python server'''
	print("py init")
	a = GameServer()


def OnServer(sockfd, type, data):
	print("OnServer:%d,%d,%s"%(sockfd,type,data))
	if type == FD_TYPE_ACCEPT:
		logger.debug('OnServer,type=FD_TYPE_ACCEPT,sock=%s'%sockfd)
		try:
			GameServer().add_rpc_channel(sockfd)
		except Exception as e:
			print("Exception:",e)
	elif type == FD_TYPE_READ:
		try:
			GameServer().recv_data(sockfd, data)
		except Exception as e:
			print("Exception:",e)
	elif type == FD_TYPE_CLOSE:
		logger.debug('OnServer,type=FD_TYPE_CLOSE,sock=%s'%sockfd)
		try:
			GameServer().del_rpc_channel(sockfd)
		except Exception as e:
			print("Exception:",e)

	return 1,"success"
