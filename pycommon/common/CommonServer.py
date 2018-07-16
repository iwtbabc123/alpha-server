from common.ProxyManager import ProxyManager
from rpc.TcpConnection import TcpConnection
from rpc.RpcChannel import RpcChannel
from defines import *

class CommonServer():
	"""通用的服务器基类"""
	def __init__(self, server_name = None):
		#self.rpc_channel_mgr = RpcChannelMgr()
		self._proxy_manager = ProxyManager()
		self.server_name = server_name
		self._client_service = None
		self._server_service = None # TODO,可能需要支持多个
		self.init_service()

	@property
	def proxy_manager(self):
		return self._proxy_manager

	def add_client_rpc_channel(self, sockfd):
		if not self._client_service:
			return
		conn = TcpConnection(sockfd, PROCESS_TYPE_CLIENT)
		rpc_channel = RpcChannel(self._client_service, conn)
		conn.attach_rpc_channel(rpc_channel)
		self.proxy_manager.set_client_rpc_channel(sockfd, rpc_channel)
	
	def add_server_rpc_channel(self, sockfd):
		if not self._server_service:
			return
		conn = TcpConnection(sockfd, PROCESS_TYPE_SERVER)
		rpc_channel = RpcChannel(self._server_service, conn)
		conn.attach_rpc_channel(rpc_channel)
		self.proxy_manager.set_server_rpc_channel(sockfd, rpc_channel)
		self.add_proxy(sockfd, rpc_channel, PROCESS_TYPE_SERVER)
	
	def del_client_rpc_channel(self, sockfd):
		self.proxy_manager.del_client_rpc_channel(sockfd)
	
	def del_server_rpc_channel(self, sockfd):
		self.proxy_manager.del_server_rpc_channel(sockfd)
	
	def handle_client_rpc_channel(self, sockfd, data):
		if not self._client_service:
			return
		print("handle_client_rpc_channel")
		rpc_channel = self.proxy_manager.get_client_rpc_channel(sockfd)
		if rpc_channel is None:
			return
		rpc_channel.conn.recv_data(data)
	
	def handle_server_rpc_channel(self, sockfd, data):
		if not self._server_service:
			return
		rpc_channel = self.proxy_manager.get_server_rpc_channel(sockfd)
		if rpc_channel is None:
			return
		rpc_channel.conn.recv_data(data)

	def init_service(self):
		'''各子类继承'''
		raise NotImplementedError

	def add_proxy(self, socketfd, rpc_channel, server_type):
		'''各子类继承'''
		raise NotImplementedError
