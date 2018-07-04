import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
import pymainbase
pymainbase.import_dir(['library','proto_python','../pyscripts/dbservice'])

from framework.DBServer import DBServer

#logger = logger.get_logger('pymain')

def init(server_name):
	'''初始化python server'''
	print("py init",server_name)
	try:
		a = DBServer(server_name)
	except Exception as e:
		print("init Exception:",e)


def OnServer(sockfd, type, data):
	serverobj = DBServer()
	pymainbase.OnServer(sockfd, type, data, serverobj)
	return 1,"success"
