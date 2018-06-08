import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/library'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../../pycommon/proto_python'))
sys.path.insert(0, join(abspath(dirname(__file__)), '../'))

from proto_python import common_pb2,client_mongo_pb2
from pb_test.tcp_client import TcpClient
import asyncore
import time
import json

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 6000

client = None
server_proxy = None

class DBServerProxy():
	'''与db通讯的proxy'''
	def __init__(self, stub):
		self.dbstub = stub
		self.connected = True
		self.findrequest = client_mongo_pb2.FindDocRequest()
		self.updaterequest = client_mongo_pb2.UpdateDocRequest()
		self.insertrequest = client_mongo_pb2.InsertDocRequest()

	def on_channel_disconnected(self, rpc_channel):
		self.connected = False
	
	def db_find_doc(self, db, collection, query, fields = None,limit = 1, callback = None):
		request = self.findrequest
		request.Clear()
		request.db = db
		request.collection = collection
		request.query = json.dumps(query)
		request.fields = json.dumps({}) if fields == None else json.dumps(fields)
		request.limit = limit
		if callback != None:
			request.callback_id = 1
		self.dbstub.db_find_doc(None, request)
	
	def db_update_doc(self, db, collection, query, doc, callback = None, upset = True, multi = False):
		request = self.updaterequest
		request.Clear()
		request.db = db
		request.collection = collection
		request.query = json.dumps(query)
		request.doc = json.dumps(doc)
		request.upset = upset
		request.multi = multi
		if callback != None:
			request.callback_id = 1
		self.dbstub.db_update_doc(None, request)
	
	def db_insert_doc(self, db, collection, doc, callback = None):
		request = self.insertrequest
		request.Clear()
		request.db = db
		request.collection = collection
		request.doc = json.dumps(doc)
		if callback != None:
			request.callback_id = 1
		self.dbstub.db_insert_doc(None, request)

# 被调用方,接收调用方(stub)的rpc请求
class MyClientService(client_mongo_pb2.IDBClientService):
	def connect_reply(self, rpc_controller, request, done):
		print("connect_reply:entityid=%s,type=%d"%(request.entityid,request.type))

		time.sleep(3)
		print("sleep 3s")
		entity_msg = common_pb2.EntityMessage()
		entity_msg.entityid = request.entityid
		entity_msg.method = "test"
		entity_msg.parameters = "none"
		client.stub.entity_message(None, entity_msg, None)
	
	def entity_message(self, rpc_controller, request, done):
		print("entity_message:entityid=%s,method=%s"%(request.entityid,request.method))
	
	def db_find_doc_reply(self, rpc_controller, request, done):
		print("db_find_doc_reply:",request.status)
		#print("db_find_doc_reply:",request.docs)
		#result = [json.loads(x) for x in request.docs]
		for x in request.docs:
			print("db_find_doc_reply:",x)
		#result = [json.loads(x) for x in request.docs]
		time.sleep(3)


	def db_update_doc_reply(self, rpc_controller, request, done):
		print("db_update_doc_reply")
	
	def db_insert_doc_reply(self, rpc_controller, request, done):
		print("db_insert_doc_reply")
		time.sleep(3)
		server_proxy.db_find_doc('test_db', 'test_collection',{"name":"mjf"})


if __name__ == "__main__":
	client = TcpClient(LISTEN_IP, LISTEN_PORT, client_mongo_pb2.IDBService_Stub, MyClientService)
	if client.sync_connect():
		server_proxy = DBServerProxy(client.stub)

		data = {"name":'mjf','province':'henan','age':25}

		server_proxy.db_insert_doc('test_db','test_collection', data)
		#request = common_pb2.ConnectServerRequest()
		#request.entityid = "1"
		#request.type = common_pb2.ConnectServerRequest.NEW_CONNECTION
		#client.stub.connect_server(None, request, None)
		asyncore.loop()
