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

def OnClientProxy(sockfd, type, data):
	serverobj = gate_server
	if serverobj is None:
		return 0, "fail"
	pymainbase.OnClientProxy(sockfd, type, data, serverobj)
	return 1,"success"

def OnServerProxy(sockfd, type, data):
	serverobj = gate_server
	if serverobj is None:
		return 0, "fail"
	pymainbase.OnServerProxy(sockfd, type, data, serverobj)
	return 1,"success"
