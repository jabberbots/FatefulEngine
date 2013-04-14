# coding: utf-8

# Message handler.
# © simpleApps

from random import choice

def msgDelivery(client, msg):
    if msg.getTag("request"):
        reportMsg = xmpp.protocol.Message(msg.getFrom())
        reportMsg.setID(msg.getID())
        reportMsg.addChild("received", namespace = "urn:xmpp:receipts")
        client.send(reportMsg)

def replaceKeys(text, conf):
	nick = getNick(conf)
	for x in (":", ",", ">"):
		x = nick + x
		if text.startswith(x):
			return text[len(x):].lstrip()
	return str()

def MessageProcess(client, msg):
	if msg.timestamp: return
	msgType = msg.getType()
	text = msg.getBody()
	if not text: return
	text = text.strip()
	fromjid = msg.getFrom()
	nick = fromjid.getResource()
	conf = fromjid.getStripped()
	simple = (fromjid, conf, nick)
## text split, replace, etc
	if msgType != "chat":
		text = replaceKeys(text, conf)
	try: body = text.lower().split()
	except: return
	if not body: return
#	if not text.startswith(getNick(conf)): return
## stop if jid = nick or jid not in JIDS/AFFILATIONS
	if nick == getNick(conf): return
	if conf not in AFFILATIONS: return
	if nick not in AFFILATIONS[conf]: return
## Start main message handler
	if msgType in ("groupchat", "chat"):
## Roster & Private messages delivery
		if msgType == "chat": msgDelivery(client, msg)
## Start commands handler
		if body[0] == CMD_JOIN:
			try:
				if not msgType == "chat": return
				if not conf in ADMINS: return
				if not len(body) > 1: 
					reply(msgType, simple, ErrorReplys[0])
					return
				if body[1].count("@") and body[1].count(".") >1:
					if body[1] in Chats:
							reply(msgType, simple, 
								JoinAnswers[1] % body[1])
					else:
						join(body[1], DefaultNick)
						reply(msgType, simple, 
							JoinAnswers[0] % body[1])
				else:
					reply(msgType, simple, JoinAnswers[2] % body[1])
			except:
				crashlog("join")
		elif body[0] == CMD_RELOAD:
			if not msgType == "chat": return
			if not conf in ADMINS: return
			die(True)
		elif body[0] == CMD_LEAVE:
			if len(body) == 1:
				if Afl(conf, nick) in ("admin", "owner"):
					leave(conf, "By command from admin")
			elif body[1].count("@") and conf in ADMINS:
				if body[1] in Chats:
					leave(body[1], "By command from admin")
					reply(msgType, simple, 
						LeaveAnswers[0] % body[1])
				else:
					reply(msgType, simple, 
						JoinAnswers[2] % body[1])
					return
			else:
				reply(msgType, simple, ErrorReplys[0])
		elif body[0] == CMD_SETNICK:
			setNick(conf, body[1])
		elif body[0] == CMD_ERR:
			try:
				if not conf in ADMINS: return
				dbody = text.split()
				if len(dbody)>1:
					if dbody[1] == CMD_CLEAN:
						fileKill(os.listdir("crashlog"), "crashlog/%s")
						reply(msgType, simple, CMD_CLEAN_Repl)
					elif dbody[1] == CMD_CRASHLIST:
						if os.path.exists("crashlog"):
							replaced = (", ".join(os.listdir("crashlog"))).replace(".txt", "")
							if not replaced:
								reply(msgType, simple, CMD_ERR_ANSWERS[1])
								return
							reply(msgType, simple, replaced)
						else:
							reply(msgType, simple, CMD_ERR_ANSWERS[1])
					else:
						log = "crashlog/%s.txt" % dbody[1]
						if os.path.exists(log):
							reply(msgType, simple, rFile(log).decode("cp1251"))
						else:
							reply(msgType, simple, CMD_ERR_ANSWERS[2])	
				else:
					reply(msgType, simple, ErrorReplys[0])	
			except: pass
		elif body[0] == "exec":
			if not conf in ADMINS: return
			reply(msgType, simple, pyExec(text[(text.find(" ") + 1):].strip()))
		elif body[0] == "eval":
			if not conf in ADMINS: return
			reply(msgType, simple, pyEval(text[(text.find(" ") + 1):].strip()))
		else:
			reply(msgType, simple, choice(rFile("other/phrases.txt").splitlines()))