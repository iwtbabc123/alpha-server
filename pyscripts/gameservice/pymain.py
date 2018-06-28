import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/library'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/proto_python'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../gameservice'))

#import logger
#from defines import *
from framework.GameServer import GameServer
import pymainbase

def init():
	'''初始化python server'''
	print("py init")
	a = GameServer()


def OnServer(sockfd, type, data):
	serverobj = GameServer()
	pymainbase.OnServer(sockfd, type, data, serverobj)
	return 1,"success"
