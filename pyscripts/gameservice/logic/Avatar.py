from common.EntityBase import EntityBase

class Avatar(EntityBase):
	'''玩家类'''
	def __init__(self, entityid):
		print("CreateNewAvatar:entityid=%s"%entityid)
		super().__init__(entityid)
	
	def save(self):
		pass

	def load(self):
		pass

	def destroy(self):
		pass
	
	def test(self):
		print("testtest")