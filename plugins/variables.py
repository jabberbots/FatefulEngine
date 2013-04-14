# coding: utf-8

## GetVariables plugin
## For Fateful Engine (for 0.5.5M and later with M)
## © simpleApps CodingTeam, 2011

__version__ = "1"

# get JID by Client
def getJid(client):
	return "%s@%s" % \
			(client._owner.User, 
			client._owner.Server)

# get Nick by conference
def getNick(conf):
	if conf in Chats:
		return Chats[conf]
	return str()

# get and set value of AFFILATIONS
def Afl(conf, nick, type = "get", afl = "wtf"):
	if type is "get": 
		return AFFILATIONS[conf][nick]
	if type is "set":
		if AFFILATIONS[conf].has_key(nick):
			del AFFILATIONS[conf][nick]
		AFFILATIONS[conf][nick] = afl

# get and set value of JIDS
def Jid(conf, nick, type = "get", jid = ""):
	if type is "get":
		return JIDS[conf][nick]
	if type is "set":
		if JIDS[conf].has_key(nick):
			del JIDS[conf][nick]
    	JIDS[conf][nick] = jid