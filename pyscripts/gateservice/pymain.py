import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
import pymainbase
pymainbase.import_dir(['library','proto_python','../pyscripts/gateservice'])

from framework.GateServer import GateServer

gate_server = None

def init(server_name):
	global gate_server
	'''初始化python server'''
	print("py init",server_name)
	gate_server = GateServer(server_name)
	#gate_serverserver.connect_server()


def OnServer(sockfd, type, data):
	serverobj = gate_server
	if serverobj is None:
		return 0, "fail"
	pymainbase.OnServer(sockfd, type, data, serverobj)
	return 1,"success"
