# coding:utf8
import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/library'))

from proto_python.echo_test_pb2 import IEchoService_Stub,IEchoClient,RequestMessage
from rpc.tcp_client import TcpClient
import asyncore

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 1888

# 被调用方,接收调用方(stub)的rpc请求
class MyEchoClientReply(IEchoClient):
	def echo_reply(self, rpc_controller, request, done):
		print("MyEchoClientReply:%s"%request.msg)
		

if __name__ == "__main__":
	request = RequestMessage()
	request.msg = "just for test"
	
	client = TcpClient(LISTEN_IP, LISTEN_PORT, IEchoService_Stub, MyEchoClientReply)
	client.sync_connect()
	
	client.stub.echo(None, request, None)
	
	asyncore.loop()