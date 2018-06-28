import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/library'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/proto_python'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../gateservice'))

import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
import pymainbase
pymainbase.import_dir(['library','proto_python','../pyscripts/gateservice'])

from framework.GateServer import GateServer

def init(server_name):
	'''初始化python server'''
	print("py init",server_name)
	a = GateServer()


def OnServer(sockfd, type, data):
	serverobj = GateServer()
	pymainbase.OnServer(sockfd, type, data, serverobj)
	return 1,"success"
