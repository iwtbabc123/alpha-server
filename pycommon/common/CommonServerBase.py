from rpc.RpcChannelMgr import RpcChannelMgr
from rpc.TcpConnection import TcpConnection
from rpc.RpcChannel import RpcChannel

class CommonServerBase():
	"""通用的服务器基类"""
	def __init__(self):
		self.rpc_channel_mgr = RpcChannelMgr()
		self.pb_service = None
	
	def set_pb_service(self, pb_service):
		self.pb_service = pb_service

	def check_pb_service(self):
		return self.pb_service is not None

	def add_rpc_channel(self, sockfd):
		if not self.check_pb_service():
			return
		print("add_rpc_channel")
		conn = TcpConnection(sockfd)
		rpc_channel = RpcChannel(self.pb_service, conn)
		conn.attach_rpc_channel(rpc_channel)
		self.rpc_channel_mgr[sockfd] = rpc_channel
	
	def del_rpc_channel(self, sockfd):
		if not self.check_pb_service():
			return
		print("del_rpc_channel")
		del self.rpc_channel_mgr[sockfd]

	def handle_rpc_channel(self, sockfd, data):
		if not self.check_pb_service():
			return
		print("recv_data")
		rpc_channel = self.rpc_channel_mgr[sockfd]
		if rpc_channel is None:
			return
		rpc_channel.conn.recv_data(data)
	
