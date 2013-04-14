# coding: utf-8

# File Killer plugin
# © simpleApps CodingTeam, 2011

def fileKill(_file, path = None):
	if type(_file) is list:
		for i in _file:
			try:
				os.remove(path % i)
			except:
				continue
		return True
	else:
		try:
			return os.remove(_file)
		except:
			return False