from framework.GameService import GameService
from common.CommonServerBase import CommonServerBase
from singleton import *

@singleton
class GameServer(CommonServerBase):
	'''python逻辑层服务器'''
	def __init__(self):
		super().__init__()
		pb_service = GameService()
		self.set_pb_service(pb_service)
	
	def tick(self):
		pass
	
