# coding:utf8

from proto_python import client_gate_pb2
from proto_python.common_pb2 import ConnectServerReply

class GateService(client_gate_pb2.IGateService):
	def __init__(self):
		pass

	def connect_server(self, controller, request, _done):
		rpc_channel = controller.rpc_channel
		entityid = request.entityid
		msg = request.authmsg
		
		response = ConnectServerReply()
		response.entityid = entityid
		response.extramsg = "echo:"+msg + str(entityid)
		
		print("response.msg:%s"%response.extramsg)

	def entity_message(self, controller, request, _done):
		pass