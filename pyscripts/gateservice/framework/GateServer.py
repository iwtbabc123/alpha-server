from framework.GateService import GateService
from common.CommonServerBase import CommonServerBase
from singleton import *

@singleton
class GateServer(CommonServerBase):
	'''python逻辑层服务器'''
	def __init__(self):
		super().__init__()
		pb_service = GateService()
		self.set_pb_service(pb_service)
	
	def tick(self):
		pass
	
