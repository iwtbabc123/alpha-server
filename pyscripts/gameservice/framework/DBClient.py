from proto_python import common_pb2,client_mongo_pb2

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
	
	def db_update_doc(self, db, collection, query, doc, callback = None, upsert = True, multi = False):
		request = self.updaterequest
		request.Clear()
		request.db = db
		request.collection = collection
		request.query = json.dumps(query)
		request.doc = json.dumps(doc)
		#request.upsert = upsert
		#request.multi = multi
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

class DBClient(client_mongo_pb2.IDBClientService):
	'''接收db发过来的消息'''
	def __init__(self, config):
		pass

	def db_find_doc_reply(self, _controller, reply, _done):
		pass
	
	def db_update_doc_reply(self, _controller, reply, _done):
		pass
	
	def db_insert_doc_reply(self, _controller, reply, _done):
		pass