from common.ProxyManager import ProxyManager
from rpc.TcpConnection import TcpConnection
from rpc.RpcChannel import RpcChannel

class CommonServerBase():
	"""通用的服务器基类"""
	def __init__(self, server_name = None, server_type = None):
		#self.rpc_channel_mgr = RpcChannelMgr()
		self._proxy_manager = ProxyManager(server_type)
		self.server_name = server_name
		self.pb_service_map = {}  # server type => pb_service
		self.init_service()

	@property
	def proxy_manager(self):
		return self._proxy_manager

	@proxy_manager.setter
	def proxy_manager(self, value):
		self._proxy_manager = value

	def set_pb_service(self, pb_service, server_type):
		self.pb_service_map[server_type] = pb_service

	def check_pb_service(self, server_type):
		return self.pb_service_map.get(server_type) is not None

	def get_pb_service(self, server_type):
		return self.pb_service_map.get(server_type)

	def add_rpc_channel(self, sockfd, server_type):
		if not self.check_pb_service(server_type):
			return
		print("add_rpc_channel")
		conn = TcpConnection(sockfd)
		rpc_channel = RpcChannel(self.get_pb_service(server_type), conn)
		conn.attach_rpc_channel(rpc_channel)
		#self.rpc_channel_mgr[sockfd] = rpc_channel
		self.proxy_manager.set_rpc_channel(sockfd, rpc_channel, server_type)
		self.add_proxy(sockfd, rpc_channel, server_type)
	
	def del_rpc_channel(self, sockfd, server_type):
		if not self.check_pb_service(server_type):
			return
		print("del_rpc_channel")
		#del self.rpc_channel_mgr[sockfd]
		self.proxy_manager.del_rpc_channel(sockfd, server_type)

	def handle_rpc_channel(self, sockfd, data, server_type):
		if not self.check_pb_service(server_type):
			return
		print("recv_data")
		rpc_channel = self.proxy_manager.get_rpc_channel(sockfd, server_type)
		#rpc_channel = self.rpc_channel_mgr[sockfd]
		if rpc_channel is None:
			return
		rpc_channel.conn.recv_data(data)

	def init_service(self):
		'''各子类继承'''
		raise NotImplementedError

	def add_proxy(self, socketfd, rpc_channel, server_type):
		'''各子类继承'''
		raise NotImplementedError
