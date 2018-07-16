"""
连接其它服务器的Proxy，及接受其它服务器的消息的Client
"""
from proto_python import common_pb2,client_server_pb2

class LogicServerProxy():
	'''与其它服务器通讯的proxy'''
	def __init__(self, rpc_channel):
		self._rpc_channel = rpc_channel
		self._stub = client_server_pb2.IServerService_Stub(rpc_channel)
	
	@property
	def rpc_channel(self):
		return self._rpc_channel

	def connect_server(self, _controller, _request):
		self._stub.connect_server(_controller, _request, None)

	def entity_message(self, _controller, _request):
		self._stub.entity_message(_controller, _request, None)
	
class LogicClient(client_server_pb2.IClientService):
	'''接收其它服务器发过来的消息'''
	def __init__(self, proxy_manager):
		self._proxy_manager = proxy_manager

	@property
	def proxy_manager(self):
		return self._proxy_manager
	
	def connect_reply(self, _controller, reply, _done):
		print("LogicClient connect_reply")
		# 找到对应的客户端rpc_chanel,发送数据给客户端
		clientid = reply.clientid
		proxy = self.proxy_manager.get_client_proxy(clientid)
		if not proxy:
			return
		proxy.connect_reply(None, reply)
	
	def entity_message(self, _controller, reply, _done):
		pass
