# /* encoding: utf-8 */

# IQ handler for Fateful engine.
# © simpleApps, 2010 - 2011.
# It is a part of Fateful Engine.

from time import gmtime, strftime

def iqProcess(client, iq):
	if iq.getType() == "get":
		nsType = iq.getQueryNS()
		if nsType in (xmpp.NS_VERSION, xmpp.NS_TIME) or iq.getTag("ping"):
			result = iq.buildReply("result")
			if nsType == xmpp.NS_VERSION:
				query = result.getTag("query")
				query.setTagData("name", u"%s with ϝateϝul Engine %s" % (ProductName, EngineVer))
				query.setTagData("version", u"%s © %s" % (ProductVer, Author))
				query.setTagData("os", os_name)
			elif nsType == xmpp.NS_TIME:
				LocTime = strftime("%a, %d %b %Y %H:%M:%S")
				GMTime = strftime("%Y%m%dT%H:%M:%S (GMT)", gmtime())
				tz = strftime("%Z")
				if NT:
					tz = tz.decode("cp1251")
				query = result.getTag("query")
				query.setTagData("utc", GMTime)
				query.setTagData("tz", tz)
				query.setTagData("display", LocTime)
		else:
			result = iq.buildReply("error")
		client.send(result)