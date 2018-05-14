from framework.GameService import GameService
from rpc.RpcChannelMgr import RpcChannelMgr
from rpc.TcpConnection import TcpConnection
from rpc.RpcChannel import RpcChannel
from singleton import *

@singleton
class GameServer():
	'''python逻辑层服务器'''
	def __init__(self):
		self.game_service = GameService()
		self.rpc_channel_mgr = RpcChannelMgr()
	
	def add_rpc_channel(self,sockfd):
		print("add_rpc_channel")
		conn = TcpConnection(sockfd)
		rpc_channel = RpcChannel(self.game_service, conn)
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
	