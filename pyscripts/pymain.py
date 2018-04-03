def init():
	'''初始化python server'''
	print("py init")


def OnServer(sockfd, type, data):
	print("OnServer:%d,%d,%s"%(sockfd,type,data))
