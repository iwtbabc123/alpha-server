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
LISTEN_PORT = 5000

client = None

# 被调用方,接收调用方(stub)的rpc请求
class MyClientService(client_server_pb2.IClientService):
	def connect_reply(self, rpc_controller, request, done):
		print("connect_reply:%s"%request.extramsg)

		time.sleep(3)
		print("connect_reply2:%s"%request.extramsg)
		request = common_pb2.EntityMessage()
		request.id = 1
		request.method = "entity_message"
		request.parameters = "none"
		client.stub.entity_message(None, request, None)
	
	def entity_message(self, rpc_controller, request, done):
		print("client:entity_message:%s"%request.method)

if __name__ == "__main__":
	client = TcpClient(LISTEN_IP, LISTEN_PORT, client_server_pb2.IServerService_Stub, MyClientService)
	if client.sync_connect():
		request = common_pb2.ConnectServerRequest()
		request.entityid = 1
		request.authmsg = "justfortest"
		client.stub.connect_server(None, request, None)
		asyncore.loop()
