#! /usr/bin/python
# /* coding: utf-8 */

# ϝateϝul engine kernel
# © simpleApps Technology, 2010 - 2011

# ϝateϝul engine distributed under Apache licence
# See the LICENCE.txt for more details

## import some modules
from time import sleep, strftime, time as Time
from platform import win32_ver
import sys, gc, os

# Enable Garbage Collection.
gc.enable()

if not (hasattr(sys, "argv") and sys.argv and sys.argv[0]):
	sys.argv = ["."]

try:
	os.chdir(os.path.dirname(sys.argv[0]))
except OSError:
	print "#! Incorrect launch!"
	sleep(5)

# NoneType objects
DispatcherStopped, Unsupported = None, None
NT, POSIX 		  = None, None # We respect Mac, but it determined as POSIX (>=10.xx).

# string objects
EngineVer 	= "0.6.5"
PIDFile 	= "other/fateful_apppid.txt"

# dict objects.
IDs 	= dict()

INFO 	=\
		{"errors": int(),
 		 "started": Time(),
		 "connected": int()}

execfile("engine.ini")

for x in modules:
	if os.path.exists(x):
		sys.path.insert(0, x) # We using insert method for get priority our libs from other.

## import from our sys.path.
try:
	import xmpp
	from sTools import *
	from writer import *
except Exception, why:
	print "#! Warning: failed to load library. Please, run engine"\
	" with parameter \"recoil\" [%s]." % why

## get your snake version ;)
snake_ver = sys.version[:3]
if float(snake_ver) < 2.6:
	Unsupported = True
	Print("#! Your Python is oldest.")

## set default encoding.
try: reload(sys).setdefaultencoding("utf-8")
except: Print("#! Can`t set default encoding!", True)

## os info.
if os.name == "nt":
	NT = True
	if not ntDetect().lower().count("windows"):
		isOS = ntDetect()
	else:
		isOS = "Windows"
	os_name = " ".join([isOS, win32_ver()[0], win32_ver()[2]])

elif os.name in ("posix", "mac"):
	POSIX 	= True
	from platform import dist
	if dist()[0]:
		os_name = "POSIX (%s with %s, %s)" % (dist()[0], 
											  os.uname()[0], os.uname()[2])
	else:
		os_name = "POSIX (%s, %s)" % (os.uname()[0], os.uname()[2])
	if os.uname()[0].lower().count("darwin"):
		print "#! Warning: The Darwin kernel poorly maintained."
else:
	os_name = os.name.upper()
	
os_name = os_name + " " + getArchitecture()
del modules, Time, ZLIBEncoder, ZLIBDecoder,\
			ntDetect, win32_ver, getArchitecture

## Working with files.
def rFile(name):
	fl = open(chkFile(name), "r")
	text = fl.read()
	fl.close()
	return text

def wFile(name, data, mode = "w"):
	fl = open(chkFile(name), mode)
	fl.write(data)
	fl.close()

def cFile(name, data = "{}"):
	name = chkFile(name)
	if os.path.exists(name): 
		return True
	try:
		folder = os.path.dirname(name)
		if folder and not os.path.exists(folder): 
			os.makedirs(folder, 0755)
		wFile(name, data)
	except: 
		crashlog("cFile")
	return True

## same adapted functions 
# (for oldest Python versions)rom our sys.path.
## os.abort
def abort(status = 1):
	for code in \
				("os.abort()", 
				 "os._exit(status)", 
				 "sys.exit(status)"):
		try: eval(code)
		except: continue

## os.system
def system(command):
	try: os.system(command)
	except: pass

## garbage collection
def GarbageCollection():
	while True is True: # We hope that it will be forever
		try:
			sys.exc_clear()
			gc.collect()
			sleep(120)
		except KeyboardInterrupt:
			if NT: 
				ntCMDColor("#bsod")
			die()

## Main Thread die.
def die(cl = None, Restart = False, Reason = None):
	if NT:
		ntCMDColor("#bsod")
	if cl and cl.isConnected():
			prs = xmpp.Presence(None, "unavailable")
			prs.setStatus(Reason or `KeyboardInterrupt`)
			cl.send(prs)
	if Restart:
		restart()
	Print("Aborting...", True); sleep(2); abort(1)

## set color of NT console.
def ntCMDColor(color):
	if color == "#red":
		system("Color 0C")
	elif color == "#green":
		system("Color 0A")
	elif color == "#blue":
		system("Color 0B")
	elif color == "#none":
		system("Color")
	elif color == "#bsod":
		system("Color 17")

## Set title of console on NT systems.
if NT:
	system("Title Fateful Engine v%s - (C) simpleApps Technology." % EngineVer)

## Work with traceback.
def crashlog(name, text = 0):
	INFO["errors"] += 1
	fiXme(name)
	try:
		File = "crashlog/%s.txt" % name
		if not os.path.exists(File): 
			cFile(File)
		if os.path.getsize(File) > CrashfileMaxSize:
			wFile(File, str())
		if crashLogEnabled:
			crashfile = open(File, "a", 0)
		else:
			crashfile = sys.stdout
		crashfile.write(strftime("| %d.%m.%Y (%H:%M:%S) |\n"))
		if text:
			crashfile.write(text)
		else:
			exc_print(None, crashfile)
		if crashLogEnabled:
			crashfile.close()
		if NT: ntCMDColor("#red")
	except Exception:
		fiXme("crashlog")
		Print(errorLog())

def errorLog():
	from traceback import format_exc
	return "\n\nError should be here:\n%s" % format_exc()

## Exec files in globals().
def MiniExec(File):
	try: 
		execfile(File, globals())
	except Exception:
		Print("MiniExec cant load file \"%s\"." % (File), True)
		crashlog("miniexec")
		Print(errorLog())

## load handlers.
def LoadHandlers(cl):
	try:
		if msgHandler:
			MiniExec("handlers/Message.py")
			cl.RegisterHandler("message", MessageProcess)
		if prsHandler:
			MiniExec("handlers/Presence.py")
			cl.RegisterHandler("presence", PresenceProcess)
		if iqHandler:
			MiniExec("handlers/IQ.py")
			cl.RegisterHandler("iq", iqProcess)
		cl.RegisterDisconnectHandler(restart)
		cl.UnregisterDisconnectHandler(cl.DisconnectHandler)
	except Exception:
		crashlog("loadhandlers")

## load plugins.
def LoadPlugins():
	if os.path.exists("plugins"):
		for plg in os.listdir("plugins"):
			if plg.lower().endswith(".py"):
				MiniExec("plugins/%s" % plg)

## new JabberID.
def Registrator(cl, jid, passw):
	try:
		printer("#-# Registration of \"%s\": ")
		username, server = jid.split("@")
		xmpp.features.register(cl, server, 
			{"username": username, "password": passw})
		printer("Ok.")
		return True
	except Exception:
		printer("Failed.")

## Restart Funct.
def restart():
	exc_print()
	printer("#! restarting")
	if NT: ntCMDColor("#blue")
	for i in xrange(5):
		sleep(1); printer(".")
	Print("\n")
	os.execl(sys.executable, sys.executable, sys.argv[0])

## get Process ID.  
def PID_Definition():
	if not os.path.exists(PIDFile):
		cFile(PIDFile, `0`)
		return
	try:
		PID = os.getpid()
		oldPID = rFile(PIDFile)
		wFile(PIDFile, `PID`)
		if oldPID != `PID`:
			printer("#-# Checking Process ID: ")
			if NT:
				kill = "taskkill /pid %s /t /f" % oldPID
				system(kill)
			else:
				try: 
					os.kill(int(oldPID), 9)
					printer("PID %s killed..." % oldPID)
				except OSError: return
	except Exception: crashlog("PID")

## dispatcher.
def dispatcher(jid, cycle = 8):
	while not DispatcherStopped:
		try: 
			IDs[jid]["Client"].Process(cycle)
		except xmpp.Conflict:
			die(IDs[jid]["Client"], 0, "Fatal exception: xmpp.Conflict. Will now halt.")
		except KeyboardInterrupt: 
			die(IDs[jid]["Client"])
		except Exception: 
			crashlog("dispatcher"); restart()

## Connect.
def isConnect(jid, password, resource, port = 5222, register = 0, UseTLS = 0, debug = []):
	if not ManyRuns: PID_Definition()
	username, server = jid.split("@")
	printer("\n#-# Connecting: ")
	IDs[jid] = dict()
	IDs[jid]["Client"] = xmpp.Client(server, port, debug)
	if UseTLS:
		Connect = IDs[jid]["Client"].connect((server, port), None, None, False)
	else:
		Connect = IDs[jid]["Client"].connect((server, port), None, False, True)
	if Connect:
		printer("ok.\n")
	else:
		if NT: ntCMDColor("#red")
		printer("Failed.\n")
		restart()
	if register:
		Registrator(IDs[jid]["Client"], jid, password)
	Auth = IDs[jid]["Client"].auth(username, password, resource)
	printer("\n#-# Auth: ")
	if not Auth:
		printer(" error (%s/%s).\n" % (`IDs[jid]["Client"].lastErr`, 
								`IDs[jid]["Client"].lastErrCode`))
		crashlog("", "auth")
		sleep(5); IDs[jid]["Client"].reconnectAndReauth()
	else:
		printer("ok.\n\n")
	IDs[jid]["Client"].sendInitPresence()
##	IDs[jid]["Client"].getRoster()
	LoadPlugins()
	return True

## Get args.
if len(sys.argv) > 1:
	if sys.argv[1] == "easter":
		import easter; easter.egg()
	elif sys.argv[1] == "help":
		Print("#-# FatefulEngine is a free engine for write jabber bots."\
			"\n\nAvailable commands:\n"\
			"* help - print this text;\n"\
			"* address to your core file;\n")
		sleep(10), abort()
	else:
		Print("#-# Arguments found. Try to exec %s." % sys.argv[1])
		globals()["__kernel__"] = sys.argv[1]

else:
	for core in os.listdir("core"):
		if core.endswith(".py"):
			globals()["__kernel__"] = core
			Print("#-# Target core: %s." % core)
			break

# Allons-y.
if __name__ == "__main__":
	try:
		MiniExec("core/%s" % __kernel__)
	except:
		exc_print()
		crashlog("__main__")