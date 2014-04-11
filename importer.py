#Set up the Django enviornment and import the data models
import urllib2
import json
import shutil

import sys, os
sys.path.append('app/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

authorsToSkip = ["presented by", "afternoon", "morning", "choir", "priesthood", "congregation", "meeting"]
namePrefixes = ["presiden", "elder", "sister", "brother", "bishop"]
from tracker.models import *

req = urllib2.Request(url='https://tech.lds.org/mc/api/conference/list',
						data='LanguageID=1')



Conferences = json.loads(urllib2.urlopen(req).read())['Conferences']
try:
	GeneralConferenceFolder = Folder.objects.get(name = "General Conference")
except:
	GeneralConferenceFolder = Folder(name = "General Conference")
	GeneralConferenceFolder.save()


for conference in Conferences:
	print conference['Title']
	try:
		ConferenceFolder = Folder.objects.get(name= conference['Title'])
		print "Session Already Imported"
		continue
	except:
		ConferenceFolder = Folder(name = conference['Title'], parentFolder = GeneralConferenceFolder)
		ConferenceFolder.save()

	req = urllib2.Request(url = 'http://tech.lds.org/mc/api/conference/sessionlist',
							data = 'ConferenceID='+str(conference['ID']))

	Sessions = json.loads(urllib2.urlopen(req).read())['Sessions']

	for session in Sessions:

		SessionFolder = Folder(name = session['Title'], parentFolder = ConferenceFolder)

		SessionFolder.save()

		req = urllib2.Request(url = 'http://tech.lds.org/mc/api/conference/talklist',
								data = 'SessionID='+str(session['ID']))

		Talks = json.loads(urllib2.urlopen(req).read())['Talks']

		for talk in Talks:
			try:
				authorName = talk['Persons'][0]['Name']
				names = authorName.split(' ', 1)

				for prefix in namePrefixes:
				
					if prefix in names[0].lower():

						authorName = names[1]

				try:
					a = Author.objects.get(name=authorName)
				except:

					skipAuthor = False
					for auth in authorsToSkip:
						
						if auth in authorName.lower():
							skipAuthor = True
							break

					if skipAuthor == True:
						continue
					else:
						a = Author(name = authorName)
						a.save()


				confTalk = ConferenceTalk(title = talk['Title'],
										 folder = SessionFolder, 
										 author = a)

				confTalk.save()

				for media in talk['Media']:
					l = Link(type = media['MediaContainer'],
					         URI = media['URL'],
					         contentItem = confTalk)
					l.save()

			except:
				continue
