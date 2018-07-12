__author__ = 'majianfei'

from proto_python import common_pb2,client_server_pb2
from common.EntityManager import EntityManager

class ClientProxy():
	def __init__(self, rpc_channel):
		self.client_stub = client_server_pb2.IClientService_Stub(rpc_channel)
	
	def connect_reply(self, controller, response):
		self.client_stub.connect_reply(controller, response, None)
	
	def entity_message(self, controller, response):
		self.client_stub.entity_message(controller, response, None)

class GameService(client_server_pb2.IServerService):
	'''实现gpb rpc service'''
	def __init__(self, proxy_manager):
		self._proxy_manager = proxy_manager

	def connect_server(self, controller, request, _done):
		rpc_channel = controller.rpc_channel
		entityid = request.entityid

		create_result = False
		if self._create_entity(entityid):
			create_result = True

		response = common_pb2.ConnectServerReply()
		response.entityid = entityid
		response.clientid = request.clientid
		if create_result:
			response.type = common_pb2.ConnectServerReply.CONNECTED
		else:
			response.type = common_pb2.ConnectServerReply.FORBIDDEN

		print("connect server response")
		client_proxy = self._get_client_proxy(rpc_channel)
		client_proxy.connect_reply(controller, response)

	def entity_message(self, controller, request, _done):
		rpc_channel = controller.rpc_channel
		entityid = request.entityid
		method = request.method
		param = request.parameters
		
		self._call_entity_method(entityid, method, param)

		response = common_pb2.EntityMessage()
		response.entityid = entityid
		response.method = "callclient"
		response.parameters = param

		print("entity message response")

		client_proxy = self._get_client_proxy(rpc_channel)
		client_proxy.entity_message(controller, response)

	def _get_client_proxy(self, rpc_channel):
		client_proxy = ClientProxy(rpc_channel)
		return client_proxy

	def _create_entity(self, entityid):
		'''创建Avatar对象'''
		from logic.Avatar import Avatar
		entity = Avatar(entityid)
		EntityManager().addentity(entityid, entity)
		return True
	
	def _call_entity_method(self, entityid, method, param):
		entity = EntityManager().getentity(entityid)
		if entity:
			getattr(entity, method)()

	