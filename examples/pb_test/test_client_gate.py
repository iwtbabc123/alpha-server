import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/library'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/proto_python'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../'))

from proto_python import common_pb2,client_server_pb2
from pb_test.tcp_client import TcpClient
import asyncore
import time

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 4000

server_proxy = None

class GateServerProxy():
	"""与GateServer通讯的proxy"""
	def __init__(self, stub):
		self.dbstub = stub
	
	def connect_server(self, controller, request, done):
		self.dbstub.connect_server(controller, request, done)
	
	def entity_message(self, controller, request, done):
		self.dbstub.entity_message(controller, request, done)

# 被调用方,接收调用方(stub)的rpc请求
class MyClientService(client_server_pb2.IClientService):
	def connect_reply(self, rpc_controller, request, done):
		print("connect_reply:entityid=%s,type=%d"%(request.entityid,request.type))
		print("connect_reply:clientid=%s"%request.clientid)
		time.sleep(3)
		print("sleep 3s")
		entity_msg = common_pb2.EntityMessage()
		entity_msg.entityid = request.entityid
		entity_msg.method = "test"
		entity_msg.parameters = "none"
		#server_proxy.entity_message(None, entity_msg, None)
	
	def entity_message(self, rpc_controller, request, done):
		print("entity_message:entityid=%s,method=%s"%(request.entityid,request.method))

if __name__ == "__main__":
	client = TcpClient(LISTEN_IP, LISTEN_PORT, client_server_pb2.IServerService_Stub, MyClientService)
	if client.sync_connect():
		server_proxy = GateServerProxy(client.stub)
		request = common_pb2.ConnectServerRequest()
		request.entityid = "1"
		request.clientid = ""
		request.type = common_pb2.ConnectServerRequest.NEW_CONNECTION
		server_proxy.connect_server(None, request, None)
		asyncore.loop()
