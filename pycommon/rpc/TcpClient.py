from defines import *
import logger
from rpc.RpcChannel import RpcChannel

class TcpClient():
	'''封装一个带rpc的client'''

	def __init__(self, sockfd, stub_factory, service_factory):
		self.logger = logger.get_logger('TcpClient')
		self.stub_factory = stub_factory
		self.service_factory = service_factory
		self.channel = None
		self.stub = None
		self.service = None
	
	def handle_connect(self):
		self.service = self.service_factory()
		self.channel = RpcChannel(self.service, self)
		self.stub = self.stub_factory(self.channel)
		