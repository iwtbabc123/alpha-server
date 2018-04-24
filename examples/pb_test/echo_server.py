# coding:utf8

import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/library'))

import asyncore
from proto_python.echo_test_pb2 import IEchoClient_Stub, IEchoService,ResponseMessage
from rpc.tcp_server import TcpServer
import logger

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 1888


# 被调用方的Service要自己实现具体的rpc处理逻辑
class MyEchoService(IEchoService):
	
	def echo(self, controller, request, done):
		
		rpc_channel = controller.rpc_channel
		msg = request.msg
		
		response = ResponseMessage()
		response.msg = "echo:"+msg
		
		print("response.msg:%s"%response.msg)
		
		# 此时，服务器是调用方，就调用stub.rpc，客户端时被调用方,实现rpc方法。
		client_stub = IEchoClient_Stub(rpc_channel)
		client_stub.echo_reply(controller, response, None)
		
		
# 主服务器
class GameServer():
	def __init__(self):
		self.logger = logger.get_logger("GameServer")
		self.server = None
	
	def run(self):
		self.server = TcpServer(LISTEN_IP, LISTEN_PORT, MyEchoService)
		

if __name__ == "__main__":
	gameserver = GameServer()
	gameserver.run()
	while True:
		asyncore.loop()
	
	