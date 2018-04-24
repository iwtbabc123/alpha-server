import logger
from defines import *

class TcpConnection():

	DEFAULT_RECV_BUFFER = 4096
	ST_INIT = 0
	ST_ESTABLISHED = 1
	ST_DISCONNECTED = 2

	def __init__(self, sockfd):
		self.logger = logger.get_logger('TcpConnection')
		self.sockfd = sockfd

		#self.writebuff = b''
		self.recv_buff_size = TcpConnection.DEFAULT_RECV_BUFFER

		self.status = TcpConnection.ST_INIT
		if sockfd:
			self.status = TcpConnection.ST_ESTABLISHED
			#self.setsockopt()

		self.rpc_channel = None

	#def setsockopt(self):
	#	self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

	def get_rpc_channel(self):
		return self.rpc_channel

	def attach_rpc_channel(self, channel_interface):
		self.rpc_channel = channel_interface

	def is_established(self):
		return self.status == TcpConnection.ST_ESTABLISHED

	def set_recv_buffer(self, size):
		self.recv_buff_size = size

	def disconnect(self):
		if self.status == TcpConnection.ST_DISCONNECTED:
			return

		if self.rpc_channel:
			self.rpc_channel.on_disconnected()
		self.rpc_channel = None

		if self.sockfd:
			pass  # 调用底层关闭socket

		self.status = TcpConnection.ST_DISCONNECTED

	def send_data(self, data):
		print("TcpConnection send_data",type(data),len(data))
		#self.writebuff += str(data, 'utf-8')
		#self.writebuff += data
		import alphaEngine
		alphaEngine.OnClient(self.sockfd, FD_TYPE_CLIENT, str(data, encoding = "utf8"))
		pass

	def recv_data(self,data):
		print("recv_data")
		if not self.rpc_channel:
			return
		print("recv_data rpc_channel")
		self.rpc_channel.input_data(data)