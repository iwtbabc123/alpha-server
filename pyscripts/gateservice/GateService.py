from proto_python.client_gate_pb2 import IGateService,IGateClient_Stub
from proto_python.common_pb2 import ConnectServerReply

class GateService(IGateService):
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

		client_stub = IGateClient_Stub(rpc_channel)
		client_stub.connect_reply(controller, response, None)

	def entity_message(self, controller, request, _done):
		pass