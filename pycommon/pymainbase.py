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

def OnClientProxy(sockfd, type, data, serverobj):
	"""收到客户端的socket请求入口"""
	print("OnClientProxy:%d,%d,%s"%(sockfd,type,data))
	if type == FD_TYPE_ACCEPT:
		logger.debug('OnClientProxy,type=FD_TYPE_ACCEPT,sock=%d'%sockfd)
		try:
			serverobj.add_client_rpc_channel(sockfd)
		except Exception as e:
			print("Exception:",e)
	elif type == FD_TYPE_CLIENT:
		logger.debug('OnServer,type=FD_TYPE_READ,sock=%s'%sockfd)
		try:
			serverobj.handle_client_rpc_channel(sockfd, data)
		except Exception as e:
			print("Exception:",e)
	elif type == FD_TYPE_CLOSE:
		logger.debug('OnServer,type=FD_TYPE_CLOSE,sock=%s'%sockfd)
		try:
			serverobj.del_client_rpc_channel(sockfd)
		except Exception as e:
			print("Exception:",e)
	elif type == FD_TYPE_TIMER:
		logger.debug('OnServer,type=FD_TYPE_TIMER,sock=%s'%sockfd)
		from common import Timer
		Timer.onTimer(sockfd)  # timerId
		
	

def OnServerProxy(sockfd, type, data, serverobj):
	"""收到服务端的socket请求入口"""
	print("OnServerProxy:%d,%d,%s"%(sockfd,type,data))
	if type == FD_TYPE_CONNECT:  # 连接其它服务器成功
		logger.debug('OnServerProxy,type=FD_TYPE_CONNECT,sock=%s'%sockfd)
		try:
			serverobj.add_server_rpc_channel(sockfd)
		except Exception as e:
			print("Exception:",e)
	elif type == FD_TYPE_SERVER:
		logger.debug('OnServerProxy,type=FD_TYPE_SERVER,sock=%s'%sockfd)
		try:
			serverobj.handle_server_rpc_channel(sockfd, data)
		except Exception as e:
			print("Exception:",e)
		