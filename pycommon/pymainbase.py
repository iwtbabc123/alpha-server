import sys
from os.path import abspath, join, dirname
import logger
from defines import *

logger = logger.get_logger('pymain')

def import_dir(dir_list):
	print("import dir")
	for dir in dir_list:
		sys.path.insert(0, join(abspath(dirname(__file__)), dir))
		print("import dir:",join(abspath(dirname(__file__)), dir))

def OnServer(sockfd, type, data, serverobj):
	"""通用的接收cpp socket请求入口"""
	print("OnServer:%d,%d,%s"%(sockfd,type,data))
	if type == FD_TYPE_ACCEPT:
		logger.debug('OnServer,type=FD_TYPE_ACCEPT,sock=%s'%sockfd)
		try:
			serverobj.add_rpc_channel(sockfd)
		except Exception as e:
			print("Exception:",e)
	elif type == FD_TYPE_READ:
		logger.debug('OnServer,type=FD_TYPE_READ,sock=%s'%sockfd)
		try:
			serverobj.handle_rpc_channel(sockfd, data)
		except Exception as e:
			print("Exception:",e)
	elif type == FD_TYPE_CLOSE:
		logger.debug('OnServer,type=FD_TYPE_CLOSE,sock=%s'%sockfd)
		try:
			serverobj.del_rpc_channel(sockfd)
		except Exception as e:
			print("Exception:",e)
	elif type == FD_TYPE_TIMER:
		logger.debug('OnServer,type=FD_TYPE_TIMER,sock=%s'%sockfd)
		from common import Timer
		Timer.onTimer(sockfd)  # timerId