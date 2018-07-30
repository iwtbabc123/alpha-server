from framework.DBService import DBService
from common.CommonServer import CommonServer
from singleton import *
import json

@singleton
class DBServer(CommonServer):
	'''python逻辑层服务器'''
	def __init__(self, server_name):
		super().__init__(server_name)
	
	def init_service(self):
		self.config = self.load_json_config()
		self.mongoconfig = self.config[self.server_name]['mongo']
		pb_service = DBService(self.mongoconfig)
		self._client_service = pb_service

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


