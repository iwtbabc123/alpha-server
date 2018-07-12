from framework.GameService import GameService
from common.CommonServerBase import CommonServerBase
from singleton import *
from defines import *

@singleton
class GameServer(CommonServerBase):
	'''python逻辑层服务器'''
	def __init__(self, server_name):
		super().__init__(server_name, SERVER_TYPE_GAME)
	
	def init_service(self):
		pb_service = GameService(self.proxy_manager)
		self.set_pb_service(pb_service, SERVER_TYPE_GATE)

	def add_proxy(self, socketfd, rpc_channel, server_type):
		pass

	def tick(self):
		pass
	
