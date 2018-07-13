import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
import pymainbase
pymainbase.import_dir(['library','proto_python','../pyscripts/gameservice'])

from framework.GameServer import GameServer
from defines import *

game_server = None

def init(server_name):
	'''初始化python server'''
	global game_server
	print("py init",server_name)
	try:
		game_server = GameServer(server_name)
	except Exception as e:
		print("Exception:",e)

def OnClientProxy(sockfd, type, data):
	serverobj = game_server
	if not serverobj:
		return 0,"fail"
	pymainbase.OnClientProxy(sockfd, type, data, serverobj)
	return 1,"success"

def OnServerProxy(sockfd, type, data):
	pass

