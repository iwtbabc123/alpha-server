from framework.GateService import GateService
from framework.LogicClient import LogicClient
from common.CommonServerBase import CommonServerBase
from singleton import *
from defines import *
import json
import py2cpp

@singleton
class GateServer(CommonServerBase):
	'''python逻辑层服务器'''
	def __init__(self, server_name):
		super().__init__(server_name, SERVER_TYPE_GATE)

		self.server_channels = {}
		self.server_stubs = {}
		
	def init_service(self):
		#设置本服service
		pb_service = GateService(self.proxy_manager)
		self.set_pb_service(pb_service,SERVER_TYPE_CLIENT)
		#设置其它服service
		self.set_pb_service(LogicClient(self.proxy_manager),SERVER_TYPE_GAME)

	def add_proxy(self, socketfd, rpc_channel, server_type):
		if server_type == SERVER_TYPE_GAME:
			proxy = LogicServerProxy(rpc_channel)
			self.proxy_manager.add_server_proxy(socketfd, proxy)

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

		connect_server_name = server_config['connect_server']
		if connect_server_name == '' or connect_server_name.lower() == 'none':
			return True

		connect_server_list = json_config[connect_server_name].split(',')

		for s_name in connect_server_list:
			s_config = json_config.get(s_name)
			if s_config is None:
				return False
			print("load_connect_server_config", s_config)

			_ip = s_config['ip'] if s_config['ip'] != '0.0.0.0' else '127.0.0.1'
			_port = s_config['port']
			py2cpp.OnConnectServer(_ip, _port)
		return True
	
