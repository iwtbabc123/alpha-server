from rpc.RpcChannelMgr import RpcChannelMgr
from proto_python import common_pb2
import random

class ProxyManager():
	"""管理和client通信的proxy,以及和server通信的proxy"""
	def __init__(self):
		self.client_rpc_channel_mgr = RpcChannelMgr()
		self.server_rpc_channel_mgr = RpcChannelMgr()

		self.server_proxy = {}  # socketfd->ServerProxy

		self.client_proxy = {}  # socketfd->ClientProxy

		#clientid会传给server并传回来，根据这个id可以找到对应的ServerProxy和对应的ClientProxy
		self.client_ids = {}  # clientid->client socketfd

		self.server_ids = {}  # clientid->server socketfd

	def get_client_rpc_channel(self, socketfd):
		return self.client_rpc_channel_mgr[socketfd]
	
	def get_server_rpc_channel(self, socketfd):
		return self.server_rpc_channel_mgr[socketfd]
	
	def set_client_rpc_channel(self, socketfd, rpc_channel):
		self.client_rpc_channel_mgr[socketfd] = rpc_channel
	
	def set_server_rpc_channel(self, socketfd, rpc_channel):
		self.server_rpc_channel_mgr[socketfd] = rpc_channel
	
	def del_client_rpc_channel(self, socketfd):
		del self.client_rpc_channel_mgr[socketfd]
	
	def del_server_rpc_channel(self, socketfd):
		del self.server_rpc_channel_mgr[socketfd]

	def add_server_proxy(self, socketfd,  proxy):
		self.server_proxy[socketfd] = proxy
	
	def select_server_proxy(self, clientid, client_socketfd):
		"""为客户端随机选择一个服务器连接"""
		if not self.server_proxy:
			return None
		socketfd = random.choice(self.server_proxy.keys())
		self.server_ids[clientid] = socketfd
		self.client_ids[clientid] = client_socketfd
		return self.server_proxy[socketfd]

	def get_server_proxy(self, clientid):
		socketfd = self.server_ids.get(clientid)
		if not socketfd:
			return None
		proxy = self.server_proxy.get(socketfd)
		return proxy
	
	def get_client_proxy(self, clientid):
		socketfd = self.client_ids.get(clientid)
		if not socketfd:
			return None
		proxy = self.client_proxy.get(socketfd)
		return proxy