import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
import pymainbase
pymainbase.import_dir(['library','proto_python','../pyscripts/gameservice'])

from framework.GameServer import GameServer
from defines import *

def init(server_name):
	'''初始化python server'''
	print("py init",server_name)
	try:
		a = GameServer(server_name)
	except Exception as e:
		print("Exception:",e)

def OnServer(sockfd, type, data):
	serverobj = GameServer()
	pymainbase.OnServer(sockfd, type, data, serverobj, SERVER_TYPE_GATE)
	return 1,"success"
