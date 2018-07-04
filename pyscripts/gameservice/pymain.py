import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
import pymainbase
pymainbase.import_dir(['library','proto_python','../pyscripts/gameservice'])

from framework.GameServer import GameServer

def init(server_name):
	'''初始化python server'''
	print("py init",server_name)
	a = GameServer(server_name)

def OnServer(sockfd, type, data):
	serverobj = GameServer()
	pymainbase.OnServer(sockfd, type, data, serverobj)
	return 1,"success"
