class EntityBase():
	'''所有Entity的基类'''
	def __init__(self, entityid = None):
		self.id = (entityid == None) and 0 or entityid