from pymongo import MongoClient
conn = MongoClient('mongodb://localhost:27017/')
db = conn.testdb
db.col.insert({"name":'mjf','province':'haha','age':25})