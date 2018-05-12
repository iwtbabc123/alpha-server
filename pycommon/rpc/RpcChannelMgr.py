class RpcChannelMgr:
	def __init__(self):
		self.rpc_channels = {}
	
	def __getitem__(self, conid):
		if conid in self.rpc_channels:
			return self.rpc_channels[conid]
		return None
	
	def __setitem__(self, conid, rpc_channel):
		self.rpc_channels[conid] = rpc_channel

	def __delitem__(self, conid):
		if conid in self.rpc_channels:
			del self.rpc_channels[conid]
	