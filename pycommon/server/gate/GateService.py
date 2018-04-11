# coding:utf8

from proto_python import client_gate_pb2

class GateService(client_gate_pb2.IGateService):
	def __init__(self):
		pass

	def connect_server(self, controller, connect_server_request, _done):
		pass

	def entity_message(self, controller, connect_server_request, _done):
		pass