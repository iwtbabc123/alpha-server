import hashlib

def hash(data):
	md5 = hashlib.md5()
	md5.update(data)
	return md5.hexdigest()