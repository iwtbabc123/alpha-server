"""
调用cpp接口
"""
import alphaEngine
from defines import *

def OnTimer(delay, interval):
	return alphaEngine.OnTimer(delay, interval)

def OnConnectServer(ip, port):
	alphaEngine.OnConnectServer(port, ip)

def OnClient(sockfd, data):
	alphaEngine.OnSocket(sockfd, FD_TYPE_CLIENT, data)

def OnServer(sockfd, data):
	alphaEngine.OnSocket(sockfd, FD_TYPE_SERVER, str(data, encoding = "utf8"))