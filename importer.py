#Set up the Django enviornment and import the data models
import urllib2
import json
import shutil

import sys, os
sys.path.append('app/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

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
				try:
					a = Author.objects.get(name=authorName)
				except:
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
