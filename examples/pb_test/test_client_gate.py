import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/library'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/proto_python'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../'))

from proto_python.client_gate_pb2 import IGateService_Stub,IGateClient
from proto_python.common_pb2 import ConnectServerRequest
from pb_test.tcp_client import TcpClient
import asyncore

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 4000

# 被调用方,接收调用方(stub)的rpc请求
class MyGateClient(IGateClient):
	def connect_reply(self, rpc_controller, request, done):
		print("MyEchoClientReply:%s"%request.extramsg)
	
	def entity_message(self, rpc_controller, request, done):
		print("client:entity_message:%"%request.method)

if __name__ == "__main__":
	request = ConnectServerRequest()
	request.entityid = 1
	request.authmsg = "justfortest"
	
	client = TcpClient(LISTEN_IP, LISTEN_PORT, IGateService_Stub, MyGateClient)
	if client.sync_connect():
		client.stub.connect_server(None, request, None)
		asyncore.loop()
