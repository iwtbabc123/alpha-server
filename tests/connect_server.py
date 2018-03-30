# coding:utf8

import time

from socket import AF_INET, SOCK_STREAM, socket
from thread import start_new
import struct, json
import sys
import time
import select

HEAD_LEN = 8

client_dict = {}


def sendData(command_id, sub_id, data):
	json_data = json.dumps(data)
	length = HEAD_LEN + len(json_data)

	data = struct.pack('!ihh', length, command_id, sub_id)
	senddata = data + json_data
	print "==============>",len(senddata)
	return senddata


def resolveRecvdata(fd):
	global client_dict

	msg = client_dict[fd]["msg"]

	#print "data",len(global_data)
	
	if len(msg) < HEAD_LEN:
		#print "error head short than 8:",len(global_data)
		return
		

	length, command, sub_id = struct.unpack('!ihh', msg[0:HEAD_LEN])
	print "receive",length,command,sub_id
	if length > 1024 or length < HEAD_LEN:
		print "error receive length:",length
		return
	if len(msg) < length:
		print "error length is to short:",len(msg)
		return
	data = msg[HEAD_LEN:length]
	
	#print "data2:",length,"-- ", len(data)

	msg = msg[length:]
	client_dict[fd]["msg"] = msg
	
	#print "json", data
	result = json.loads(data)
	
	print "---",result
	
	resolveRecvdata(fd)


def receiveMessage(epoll_fd):
	global client_dict

	while 1:
		print "epoll list before:"
		epoll_list = epoll_fd.poll()
		for fd, events in epoll_list:
			#print "epoll list :", fd, events
			if select.EPOLLIN & events:
				_client = client_dict[fd]["fd"]
				msg = client_dict[fd]["msg"]
				data = _client.recv(1024)
				#print "data:",data
				msg += data
				client_dict[fd]["msg"] = msg
				#print "data:", client_dict[fd]["msg"]
				resolveRecvdata(fd)


		#for idx, connection in enumerate(connections):
		#message = connection.recv(1024)
		#print "message:",message
		#global_data += message
		#resolveRecvdata()
		#time.sleep(0.2)

HOST = '127.0.0.1'
PORT = 4001
ADDR = (HOST, PORT)



epoll_fd = select.epoll()

#uniqid = 2

if __name__ == "__main__":
	args = sys.argv
	servername = None
	config = None

	#print "len args:",len(args),args
	#if len(args) < 2:
	#	raise Exception("error")

	#uniqid = int(args[1])
	start_new(receiveMessage, (epoll_fd,))

	print "now login"
	#data = {"id":uniqid, "uid":"abcdefg"}
	#client.sendall(sendData(1, 12, data))  #
	
	_client = socket(AF_INET, SOCK_STREAM)
	_addr = (HOST, PORT)
	_client.connect(_addr)

	time.sleep(5)
