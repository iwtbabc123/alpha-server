from framework.DBService import DBService
from rpc.RpcChannelMgr import RpcChannelMgr
from rpc.TcpConnection import TcpConnection
from rpc.RpcChannel import RpcChannel
from singleton import *
import json

@singleton
class DBServer():
	'''python逻辑层服务器'''
	def __init__(self):
		self.config = self.load_json_config()
		self.mongoconfig = self.config['db1']['mongo']
		self.db_service = DBService(self.mongoconfig)
		self.rpc_channel_mgr = RpcChannelMgr()
	
	def add_rpc_channel(self,sockfd):
		print("add_rpc_channel")
		conn = TcpConnection(sockfd)
		rpc_channel = RpcChannel(self.db_service, conn)
		conn.attach_rpc_channel(rpc_channel)
		self.rpc_channel_mgr[sockfd] = rpc_channel
	
	def recv_data(self,sockfd, data):
		print("recv_data")
		rpc_channel = self.rpc_channel_mgr[sockfd]
		if rpc_channel is None:
			return
		rpc_channel.conn.recv_data(data)
	
	def del_rpc_channel(self,sockfd):
		print("del_rpc_channel")
		del self.rpc_channel_mgr[sockfd]
	
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


