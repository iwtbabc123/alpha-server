from framework.GameService import GameService
from common.CommonServer import CommonServer
from singleton import *
from defines import *

@singleton
class GameServer(CommonServer):
	'''python逻辑层服务器'''
	def __init__(self, server_name):
		super().__init__(server_name)
	
	def init_service(self):
		pb_service = GameService(self.proxy_manager)
		self._client_service = pb_service

	def add_proxy(self, socketfd, rpc_channel, server_type):
		pass

	def tick(self):
		pass
	
