__author__ = 'majianfei'

from proto_python import common_pb2,client_mongo_pb2
from common.EntityManager import EntityManager
from common.MongoClientProxy import MongoClientProxy
from defines import *

class DBClientProxy():
	'''db server reply to client'''
	def __init__(self, rpc_channel):
		self.client_stub = client_mongo_pb2.IDBClientService_Stub(rpc_channel)
		self.findreply = client_mongo_pb2.FindDocReply()
		self.updatereply = client_mongo_pb2.UpdateDocReply()
		self.insertreply = client_mongo_pb2.InsertDocReply()
		self.connected = True
	
	def connect_reply(self, controller, response):
		self.client_stub.connect_reply(controller, response, None)
	
	def entity_message(self, controller, response):
		self.client_stub.entity_message(controller, response, None)

	def db_find_doc_reply(self, callback_id, status, docs = None):
		if not self.connected:
			return
		self.findreply.Clear()
		self.findreply.callback_id = callback_id
		self.findreply.status = status
		if docs != None:
			for doc in docs:
				self.findreply.docs.append(doc)
		self.client_stub.db_find_doc_reply(None, self.findreply)

	def db_update_doc_reply(self, callback_id, status):
		if not self.connected:
			return
		self.updatereply.Clear()
		self.updatereply.callback_id = callback_id
		self.updatereply.status = status
		self.client_stub.db_update_doc_reply(None, self.updatereply)
	
	def db_insert_doc_reply(self, callback_id, status, insert_id = None):
		if not self.connected:
			return
		self.insertreply.Clear()
		self.insertreply.callback_id = callback_id
		self.insertreply.status = status
		self.client_stub.db_insert_doc_reply(None, self.insertreply)

	def on_channel_disconnected(self, _rpc_channel):
		self.connected = False

class DBService(client_mongo_pb2.IDBService):
	'''rpc service'''
	def __init__(self, mongoconfig):
		self.clientproxies = {}
		self.mongoconfig = mongoconfig
		self.mongoproxy = MongoClientProxy(self.mongoconfig)
		self.mongoproxy.connect_mongo()

	def _db_reply_cb(self, optype, oprequest, clientproxy, status, result):
		'''db操作的reply'''
		print("db_reply_cb:",optype, status)
		if optype == FIND_DOC_OP:
			clientproxy.db_find_doc_reply(oprequest.callback_id, sttus, result)
		elif optype == UPDATE_DOC_OP:
			clientproxy.db_update_doc_reply(oprequest.callback_id, status)
		elif optype == INSERT_DOC_OP:
			clientproxy.db_insert_doc_reply(oprequest.callback_id, status)
		else:
			print("db reply cb error:",optype)

	def connect_server(self, controller, request, _done):
		rpc_channel = controller.rpc_channel
		entityid = request.entityid

		create_result = False
		if self._create_entity(entityid):
			create_result = True

		response = common_pb2.ConnectServerReply()
		response.entityid = entityid
		if create_result:
			response.type = common_pb2.ConnectServerReply.CONNECTED
		else:
			response.type = common_pb2.ConnectServerReply.FORBIDDEN

		print("connect server response")
		client_proxy = self._get_client_proxy(rpc_channel)
		client_proxy.connect_reply(controller, response)

	def entity_message(self, controller, request, _done):
		rpc_channel = controller.rpc_channel
		entityid = request.entityid
		method = request.method
		param = request.parameters
		
		self._call_entity_method(entityid, method, param)

		response = common_pb2.EntityMessage()
		response.entityid = entityid
		response.method = "callclient"
		response.parameters = param

		print("entity message response")

		client_proxy = self._get_client_proxy(rpc_channel)
		client_proxy.entity_message(controller, response)

	def db_find_doc(self, controller, request, _done):
		print("db_find_doc")
		rpc_channel = controller.rpc_channel
		clientproxy = self._get_client_proxy(rpc_channel)
		self._do_mongoclient_op(FIND_DOC_OP, request, clientproxy)
	
	def db_update_doc(self, controller, request, _done):
		print("db_update_doc")
		rpc_channel = controller.rpc_channel
		clientproxy = self._get_client_proxy(rpc_channel)
		self._do_mongoclient_op(UPDATE_DOC_OP, request, clientproxy)
	
	def db_insert_doc(self, controller, request, _done):
		print("db_insert_doc")
		rpc_channel = controller.rpc_channel
		clientproxy = self._get_client_proxy(rpc_channel)
		self._do_mongoclient_op(INSERT_DOC_OP, request, clientproxy)

	def _do_mongoclient_op(self, optype, oprequest, clientproxy):
		self.mongoproxy.do_db_op(optype, oprequest, clientproxy,lambda status, result:self._db_reply_cb(optype, oprequest, clientproxy, status, result))

	def _get_client_proxy(self, rpc_channel):
		client_proxy = DBClientProxy(rpc_channel)
		return client_proxy

	def _create_entity(self, entityid):
		'''创建Avatar对象'''
		from logic.Avatar import Avatar
		entity = Avatar(entityid)
		EntityManager().addentity(entityid, entity)
		return True
	
	def _call_entity_method(self, entityid, method, param):
		entity = EntityManager().getentity(entityid)
		if entity:
			getattr(entity, method)()

	