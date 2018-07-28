__author__ = "majianfei"

from singleton import *

@singleton
class EntityManager:
	'''管理所有entity的管理器'''
	def __init__(self):
		self._entities = {}
	
	def hasentity(self, entityid):
		return entityid in self._entities
	
	def getentity(self, entityid):
		return self._entities.get(entityid)
	
	def addentity(self, entityid, entity, override = False):
		self._entities[entityid] = entity