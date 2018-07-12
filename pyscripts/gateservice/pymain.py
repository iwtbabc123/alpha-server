import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
import pymainbase
pymainbase.import_dir(['library','proto_python','../pyscripts/gateservice'])

from framework.GateServer import GateServer
from defines import *

gate_server = None

def init(server_name):
	'''初始化python server'''
	global gate_server
	print("py init",server_name)
	try:
		gate_server = GateServer(server_name)
		gate_server.connect_server()
	except Exception as e:
		print("Exception:",e)


def OnServer(sockfd, type, data):
	serverobj = gate_server
	if serverobj is None:
		return 0, "fail"
	if type in [FD_TYPE_ACCEPT, FD_TYPE_CLIENT, FD_TYPE_CLOSE]:
		server_type = SERVER_TYPE_CLIENT
	elif type in [FD_TYPE_CONNECT, FD_TYPE_SERVER]:
		server_type = SERVER_TYPE_GAME
	else:
		server_type = None
	pymainbase.OnServer(sockfd, type, data, serverobj, server_type)
	return 1,"success"
