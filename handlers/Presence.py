# /* coding: utf-8 */

# Presence handler
# © simpleApps

AFFILATIONS = {}

def PresenceProcess(client, prs):
	pType = prs.getType()
	if pType in ('available', None):
		fromjid = prs.getFrom()
		conf = fromjid.getStripped() # jid in roster
		nick = fromjid.getResource()
		if not nick: 
			return
		if conf not in AFFILATIONS: AFFILATIONS[conf] = {}
## get info about user
		afl = prs.getAffiliation()
		role = prs.getRole()
		Print("afl: %s; role: %s; nick: %s" % (afl, role, nick))
		if nick not in AFFILATIONS[conf]:
			Afl(conf, nick, "set", afl)
		if not AFFILATIONS[conf][nick] == afl:
			Afl(conf, nick, "set", afl)

	if pType == "unavailable":
		scode = prs.getStatusCode()
		fromjid = prs.getFrom()
		conf = fromjid.getStripped()
		afl = prs.getAffiliation()
		nick = fromjid.getResource()
		role = prs.getRole()
		Print("pType unavailabe; сode \"%s\" in room \"%s\"; nick: %s, afl: %s, role: %s" % (
										(scode, conf, nick, afl, role)))

## what to do if ptype is error
	if pType == "error":
		ecode = prs.getErrorCode()
		fromjid = prs.getFrom()
		conf = fromjid.getStripped()
		afl = prs.getAffiliation()
		nick = fromjid.getResource()
		role = prs.getRole()
		if ecode == "409":
			fromjid = prs.getFrom()
			conf = fromjid.getStripped()
			join(conf, getNick(client) + ".")
		else:
			Print("pType error; сode \"%s\" in room \"%s\"; nick: %s, afl: %s, role: %s" % (
										(ecode, conf, nick, afl, role)))
    
## Authorize and Subscribe 
	elif pType == "subscribe":
		fromjid = prs.getFrom()
		conf = fromjid.getStripped()
		if conf in ADMINS:
			IDs[getJid(client)]["Client"].Roster.Authorize(conf)
			IDs[getJid(client)]["Client"].Roster.Subscribe(conf)
