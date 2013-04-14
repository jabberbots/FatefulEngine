# /* coding: utf-8 */
# © simpleApps, 2010 - 2011.

## strings :)
Chatsfile = "files/confs.txt"
cfg = "other/config.txt"

# ver, name and author of this product
Author = "simpleApps"
ProductName = "FE Example"
ProductVer = "4.2"

MiniExec(cfg)
MiniExec("langs/language_%s.py" % BotLanguage.upper())

Chats = {}

## Send message.
def reply(msgType, toJID, text):
	if not isinstance(text, unicode):
		text = text.decode("utf8", "replace")
	if msgType == "groupchat":
		message = xmpp.Message(toJID[1])
		text = u"%s: %s" % (toJID[2], text)
	else:
		message = xmpp.Message(toJID[0])
	message.setType(msgType)
	message.setBody(text)
	Client.send(message)

## work with confs
def conflist(conf, nick, leave = False):
	if not os.path.exists(Chatsfile):
		cFile(Chatsfile, "{}")
	cList = eval(rFile(Chatsfile))
	if leave:
		if conf in cList:
			del cList[conf]
	else:
		cList[conf] = nick
	wFile(Chatsfile, str(cList))
 
def setNick(conf, nick):
	Chats[conf] = nick
	conflist(conf, nick)
	join(conf, nick)

def join(conf, nick):  
	prs = xmpp.protocol.Presence(u"%s/%s" % (conf, nick))
	pres = prs.setTag("x", namespace = xmpp.NS_MUC)
	pres.addChild("history", {'maxchars':'0'})
	prs.setShow("chat")
	Client.send(prs)
	if conf not in Chats:
		Chats[conf] = nick
		conflist(conf, nick)

def leave(conf, status = None, really = True):
	if conf in Chats: conflist(conf, "", really)
	prs = xmpp.Presence(conf, "unavailable")
	if status: prs.setStatus(status)
	Client.send(prs)

def myjoin():
    if not os.path.exists(Chatsfile):
        cFile(Chatsfile)
    cList = eval(rFile(Chatsfile))
    for conf in cList.keys():
        join(conf, cList[conf])
        Print('#-# %s joined in %s' % (cList[conf], conf))
    return True

import threading  
## main funct.
def main():
	if isConnect(JID, Password, Resource, Port, Register, UseTLS, Debug):
		LoadHandlers(Client), join(DefaultConference, DefaultNick), myjoin()
		if NT: ntCMDColor("#green")
		Print(u"\n#-# %s BOT is ready to work!" % ProductName)
		for x in Admins:
			Client.Roster.Subscribe(x)
			Client.Roster.Authorize(x)
		threading.Thread(None, GarbageCollection, GarbageCollection, (), ) .start()
		dispatcher(JID)

## starting       
try: main()
except KeyboardInterrupt: die()
except: crashlog("system"), restart()