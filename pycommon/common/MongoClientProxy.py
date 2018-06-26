from pymongo import MongoClient
from defines import *
from bson.json_util import loads,dumps

class MongoClientProxy:
	def __init__(self, mongoconfig):
		self.mongoconfig = mongoconfig
		self.mongoclient = None
		self.connected = False
	
	def connect_mongo(self):
		mongo_ip = self.mongoconfig['ip']
		mongo_port = self.mongoconfig['port']
		username = self.mongoconfig.get('user', None)
		password = self.mongoconfig.get('pwd', None)
		database = self.mongoconfig.get('db', None)

		try:
			self.mongoclient = MongoClient(mongo_ip, mongo_port, w = 1)
			if username:
				pass
			self.connected = True
		except Exception as e:
			print("connect mongo false:",e)
		
	def do_db_op(self, optype, oprequest, clientproxy, callback):
		if self.connected:
			flag,result = self._do_db_op(optype, oprequest, clientproxy)
			callback(flag, result)
		else:
			print("do db op false")

	def _do_db_op(self, optype, oprequest, clientproxy):
		db_name = oprequest.db
		collection_name = oprequest.collection

		collection = self.mongoclient[db_name][collection_name]

		if optype == FIND_DOC_OP:
			fields = None
			query = loads(oprequest.query)
			fieldsdict = loads(oprequest.fields)
			fields = fieldsdict.get("f",None)
			kwargs = {}
			try:
				findresult = list(collection.find(query, fields, 0, int(oprequest.limit),True, False, False, False, **kwargs))
			except Exception as e:
				print("collection find error,",e)
				return False,None
			return True, findresult
		elif optype == UPDATE_DOC_OP:
			query = loads(oprequest.query)
			doc = loads(oprequest.doc)
			if '_id' in doc:
				del doc['_id']
			print("UPDATE_DOC_OP:",dumps(doc))
			#upsert = oprequest.upsert
			#multi = oprequest.multi
			try:
				collection.update(query, doc, upsert = True, multi = True)
			except Exception as e:
				print("collection update error,",e)
				return False, None
			return True, None
		elif optype == INSERT_DOC_OP:
			doc = loads(oprequest.doc)
			print("INSERT_DOC_OP:",dumps(doc))
			try:
				ret_id = collection.insert(doc)
			except Exception as e:
				print("collection insert error,",e)
				return False, None
			return True, ret_id
		else:
			#error
			print("do op db error type")
			pass
			


