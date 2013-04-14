# -*- coding: utf-8 -*-
# © idea, code, support by simpleApps
# © 2010 03.09.10 (7:36 AM)

# please, if you translate this bot to other language
# join to conference simpleApps@conference.jabber.ru 
# & send yor translation to us

# translator`s nick & language

INITIALS = u"simpleApps_CodingTeam [RU]" # only ONE space; space is a separator between nick and [language]

## statuses, reasoons

LEAVE_REASON = u"Ошибка %s. Я вынужден выйти из конференции «%s»."


## System.

CMD_RELOAD = u"релоад"

CMD_JOIN = u"джойн"

CMD_ERR = u"крэш"

CMD_LEAVE = u"выйди"

CMD_SETNICK = u"ботник"

CMD_CLEAN = u"очистить"

CMD_CRASHLIST = u"лист"

CMD_CLEAN_Repl = u"Очищено."

CMD_LJ_Repl = (u"Выхожу по команде %s", u"Я пришёл по команде %s")
                   
ADMCOMMANDS_ANSWERS = (u"Отказано в доступе.",
					   u"Не-не, ты ошибся ботом.",
					   u"Меня учили не разговаривать с незнакомцами...")
  
JoinAnswers = (u"Я зашёл в «%s»", 
			   u"Я уже сижу в «%s»", 
			   u"Странное у тебя понятие конференции. " \
			   u"Как ни крути, «%s» не похоже на конференцию.")

LeaveAnswers = (u"Меня больше нет в «%s».", )

ErrorReplys = (u"Отсутствие параметров меня огорчает.", )

CMD_ERR_ANSWERS = (u"Ошибка. Возможно этого файла нет в списке." \
                   u"Воспользуйтесь командой «крэш лист»",			# 0
                   u"Ни одного файла не найдено...",				# 1
                   u"Ошибка. Этого файла нет в списке.\n"			# 2
                   u"Воспользуйтесь командой «крэш лист».")
