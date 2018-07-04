from framework.GateService import GateService
from common.CommonServerBase import CommonServerBase
from singleton import *
import py2cpp

@singleton
class GateServer(CommonServerBase):
	'''python逻辑层服务器'''
	def __init__(self, server_name):
		super().__init__(server_name)
		pb_service = GateService()
		self.set_pb_service(pb_service)

	def tick(self):
		pass

	def connect_server(self):
		import os
		print("dir:",os.getcwd())

		f = open("config.json","r")
		text = f.read()
		f.close()

		json_config = json.loads(text)

		server_config = json_config.get(self.server_name)
		if server_config is None:
			return False
		print("load_json_config",server_config)

		connect_server_name = server_config['connecter_server']
		if connect_server_name == '' || connect_server_name.lower() == 'none':
			return True

		connect_server_list = server_config[connect_server_name].split(',')

		import py2cpp
		for s_name in connect_server_list:
			s_config = json_config.get(s_name)
			if s_config is None:
				return False
			print("load_connect_server_config", s_config)

			_ip = s_config['ip']
			_port = s_config['port']
			py2cpp.OnConnectServer(_ip, _port)
		return True

		
		return content
	
