__author__ = 'majianfei'

from proto_python import common_pb2,client_server_pb2
#from proto_python.common_pb2 import ConnectServerReply

class ClientProxy():
	def __init__(self, rpc_channel):
		self.client_stub = client_server_pb2.IClientService_Stub(rpc_channel)
	
	def connect_reply(self, controller, response):
		self.client_stub.connect_reply(controller, response, None)
	
	def entity_message(self, controller, response):
		self.client_stub.entity_message(controller, response, None)

class GameService(client_server_pb2.IServerService):
	def __init__(self):
		pass

	def connect_server(self, controller, request, _done):
		rpc_channel = controller.rpc_channel
		entityid = request.entityid
		msg = request.authmsg
		
		response = common_pb2.ConnectServerReply()
		response.entityid = entityid
		response.extramsg = "echo:"+msg + str(entityid)
		
		print("response.msg:%s"%response.extramsg)

		client_proxy = self._get_client_proxy(rpc_channel)
		client_proxy.connect_reply(controller, response)

	def entity_message(self, controller, request, _done):
		rpc_channel = controller.rpc_channel
		entityid = request.id
		msg = request.method
		para = request.parameters
		
		response = common_pb2.EntityMessage()
		response.id = entityid
		response.method = "echo:"+msg + str(entityid)
		response.parameters = para
		
		print("response.msg:%s"%response.method)

		client_proxy = self._get_client_proxy(rpc_channel)
		client_proxy.entity_message(controller, response)

	def _get_client_proxy(self, rpc_channel):
		client_proxy = ClientProxy(rpc_channel)
		return client_proxy