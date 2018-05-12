def singleton(cls):
	instance = None
	def wrapper(*args, **kwargs):
		nonlocal instance
		if instance is None:
			instance = cls(*args, **kwargs)
		return instance

	return wrapper
