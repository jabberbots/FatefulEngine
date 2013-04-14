# coding: utf-8

# Python plugin for FE.
# © simpleApps CodingTeam, 2011

def returnExc():
	from sys import exc_info
	if exc_info()[0] or exc_info()[1]:
		error = "error: %s" % \
			str(exc_info()[0])+" - "+str(exc_info()[1])
	else:
		return None
	del exc_info
	return error

def pyEval(_script):
	try:
		return `eval(unicode(_script))`
	except:
		return returnExc()


def pyExec(_script):
	_script += "\n"
	try:
		exec (unicode(_script), globals())
		return "Execced."
	except:
		return returnExc()