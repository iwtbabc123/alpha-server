from framework.DBService import DBService
from common.CommonServerBase import CommonServerBase
from singleton import *
import json

@singleton
class DBServer(CommonServerBase):
	'''python逻辑层服务器'''
	def __init__(self):
		super().__init__()
		self.config = self.load_json_config()
		self.mongoconfig = self.config['db1']['mongo']
		pb_service = DBService(self.mongoconfig)
		self.set_pb_service(pb_service)
	
	def tick(self):
		pass
	
	def load_json_config(self):
		import os
		print("dir:",os.getcwd())

		f = open("config.json","r")
		text = f.read()
		f.close()

		content = json.loads(text)
		print("load_json_config",content)
		return content


