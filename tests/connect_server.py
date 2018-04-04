# coding:utf8

import time

from socket import AF_INET, SOCK_STREAM, socket
import struct, json
import sys
import time
import select

HEAD_LEN = 8

client_dict = {}


def sendData(command_id, sub_id, data):
	json_data = json.dumps(data)

	return json_data

HOST = '127.0.0.1'
PORT = 4002
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
	#start_new(receiveMessage, (epoll_fd,))

	print("now login")
	data = {"id":123, "uid":"abcdefg"}
	#client.sendall(sendData(1, 12, data))  #

	_client = socket(AF_INET, SOCK_STREAM)
	_addr = (HOST, PORT)
	_client.connect(_addr)
	_client.sendall(str.encode("abcdefg"))

	time.sleep(10)
