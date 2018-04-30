# coding:utf8
from google.protobuf import service
from rpc.RpcController import RpcController
import struct
import logger


class RpcChannel(service.RpcChannel):
	def __init__(self, rpc_service, conn):
		super(RpcChannel, self).__init__()
		self.logger = logger.get_logger("RpcChannel")
		self.rpc_service = rpc_service
		self.conn = conn
		
		self.rpc_controller = RpcController(self)
		print("RpcChannel init")
	
	def set_rpc_service(self, rpc_service):
		self.rpc_service = rpc_service
	
	def CallMethod(self, method_descriptor, rpc_controller,
                 request, response_class, done):
		print("RpcChannel CallMethod")
		index = method_descriptor.index
		data = request.SerializeToString()
		total_len = len(data) + 6
		self.logger.debug("CallMethod:%d,%d,%s"%(total_len,index,data))
		print("typeofdata",type(data))
		
		self.conn.send_data(b''.join([struct.pack('!ih', total_len, index), data]))
		
	def input_data(self, data):
		print("input_data:%d"%len(data))
		print("typeofdata",type(data))
		if isinstance(data, str):
			data = bytes(data, encoding = "utf8")
		print("typeofdata",type(data),len(data))
		total_len, index = struct.unpack('!ih', data[0:6])
		#self.logger.debug("input_data:%d,%d" % (total_len, index))
		print("input_data:%d,%d"%(total_len, index))
		rpc_service = self.rpc_service
		s_descriptor = rpc_service.GetDescriptor()
		method = s_descriptor.methods[index]
		try:
			print("111")
			request = rpc_service.GetRequestClass(method)()
			print("111")
			serialized = data[6:total_len]
			print("111")
			request.ParseFromString(serialized)
			print("111",type(method),type(request))
			rpc_service.CallMethod(method, self.rpc_controller, request, None)
			print("111")
			
		except Exception as e:
			self.logger.error("Call rpc method failed!")
			print("error:%s"%e)
			self.logger.log_last_except()
		return True
	
	def on_disconnected():
		pass