# coding:utf8
from google.protobuf import service
from rpc.RpcController import RpcController
import struct
import logger

PACKAGE_HEAD = '!ih'
PACKAGE_HEAD_LENGTH = struct.calcsize(PACKAGE_HEAD)

class Buffer():
    def __init__(self):
        self.buff = b''
        self.logger = logger.get_logger("Buffer")

    def parse_data(self, rpc_service, data):
        self.buff += data
        buff_length = len(self.buff)
        rpc_calls = None
        for i in range(buff_length):  # use for instead of while
            if buff_length <= PACKAGE_HEAD_LENGTH:
                break
            package_length, index = struct.unpack(PACKAGE_HEAD, self.buff[:PACKAGE_HEAD_LENGTH])
            if buff_length < package_length:
                break
            s_descriptor = rpc_service.GetDescriptor()
            if index < len(s_descriptor.methods):
                method = s_descriptor.methods[index]
                request = rpc_service.GetRequestClass(method)()
                if request:
                    try:
                        serialized = self.buff[PACKAGE_HEAD_LENGTH:package_length]
                        request.ParseFromString(serialized)
                    except Exception as e:
                        self.logger.error('Buffer.parse_data, error=%s'%e)
                    else:
                        rpc_calls = rpc_calls or []
                        rpc_calls.append(method)
                        rpc_calls.append(request)
            self.buff = self.buff[package_length:]
            buff_length = buff_length - package_length
        return rpc_calls

class RpcChannel(service.RpcChannel):
    '''要好好设计rpc_channel与conn的关系'''
    def __init__(self, rpc_service, conn):
        super(RpcChannel, self).__init__()
        self.logger = logger.get_logger("RpcChannel")
        self.rpc_service = rpc_service
        self.conn = conn

        self.rpc_controller = RpcController(self)
        self.buff = Buffer()

    def set_rpc_service(self, rpc_service):
        self.rpc_service = rpc_service

    def CallMethod(self, method_descriptor, rpc_controller,
                 request, response_class, done):
        index = method_descriptor.index
        data = request.SerializeToString()
        package_length = PACKAGE_HEAD_LENGTH + len(data)
        self.logger.debug("RpcChannel.CallMethod, index:%s, data:%s"%(index, data))
        self.conn.send_data(b''.join([struct.pack(PACKAGE_HEAD, package_length, index), data]))

    def input_data(self, data):
        self.logger.debug("RpcChannel.input_data, length:%d, type:%s"%(len(data), type(data)))
        data_type = type(data)
        if data_type == str:
            data = bytes(data, encoding = "utf8")
        elif data_type != bytes:
            self.logger.error('RpcChannel.input_data: expect bytes but got %s'%type(data))
            return False
        rpc_service = self.rpc_service
        try:
            rpc_calls = self.buff.parse_data(rpc_service, data)
        except Exception as e:
            self.logger.error("RpcChannel.input_data, phase rpc method failed! msg:%s"%e)
            return False

        if rpc_calls:
            rpc_controller = self.rpc_controller
            for i in range(0, len(rpc_calls), 2):
                try:
                    method = rpc_calls[i]
                    request = rpc_calls[i+1]
                    rpc_service.CallMethod(method, rpc_controller, request, None)
                except Exception as e:
                    self.logger.error("RpcChannel.input_data, call rpc method failed!")
        return True

    def on_disconnected():
        pass

