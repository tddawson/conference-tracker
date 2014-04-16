#Set up the Django enviornment and import the data models
import urllib2
import json
import logging

import sys, os
sys.path.append('app/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from tracker.models import *

class Importer:

    def __init__(self):
        logging.basicConfig(filename='importer.log', level=logging.INFO)
        self.authorsToSkip = ["presented by", "afternoon", "morning", "choir", "priesthood", "congregation", "meeting"]
        self.namePrefixes = ["president", "elder", "sister", "brother", "bishop"]

    def run(self):
        conferenceListEndpoint = 'https://tech.lds.org/mc/api/conference/list'
        logging.info("Importing from {}".format(conferenceListEndpoint))
        req = urllib2.Request(url=conferenceListEndpoint,
						        data='LanguageID=1')

        conferenceList = self.getResponseJson(req)
        Conferences = conferenceList['Conferences']
        try:
            GeneralConferenceFolder = Folder.objects.get(name = "General Conference")
        except:
            GeneralConferenceFolder = Folder(name = "General Conference")
            GeneralConferenceFolder.save()


        for conference in Conferences:
            logging.info(conference['Title'])
            try:
                ConferenceFolder = Folder.objects.get(name= conference['Title'])
                logging.info("Session Already Imported")
                continue
            except:
                ConferenceFolder = Folder(name = conference['Title'], parentFolder = GeneralConferenceFolder)
                ConferenceFolder.save()

            req = urllib2.Request(url = 'http://tech.lds.org/mc/api/conference/sessionlist',
                                    data = 'ConferenceID='+str(conference['ID']))

            Sessions = self.getResponseJson(req)['Sessions']

            for session in Sessions:

                SessionFolder = Folder(name = session['Title'], parentFolder = ConferenceFolder)

                SessionFolder.save()

                req = urllib2.Request(url = 'http://tech.lds.org/mc/api/conference/talklist',
                                        data = 'SessionID='+str(session['ID']))

                talkList = self.getResponseJson(req)
                Talks = talkList['Talks']

                for talk in Talks:
                    try:
                        authorName = talk['Persons'][0]['Name']
                        names = authorName.split(' ', 1)

                        for prefix in self.namePrefixes:

                            if prefix in names[0].lower():

                                authorName = names[1]

                        try:
                            a = Author.objects.get(name=authorName)
                        except:

                            skipAuthor = False
                            for auth in self.authorsToSkip:

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
                            try:
                                contentFormat = ContentFormat.objects.get(container = media['MediaContainer'])
                            except:
                                contentFormat = ContentFormat(  type = media['MediaType'],
                                                                container = media['MediaContainer'])
                                contentFormat.save()

                            l = Link(format = contentFormat,
                                     URI = media['URL'],
                                     contentItem = confTalk)
                            l.save()
                        '''
                        #Generate LDS.org url
                        try:
                            contentFormat = ContentFormat.objects.get(container = 'LDS.org')
                        except:
                            contentFormat = ContentFormat(  type = 'Text',
                                                            container = 'LDS.org')
                            contentFormat.save()

                        conf = talkList['Conference']
                        year = conf['Year']
                        month = '{num:02d}'.format(num = conf['Month'])
                        scrubbedName = talk['Title']
                        uri = 'https://www.lds.org/general-conference/{}/{}/{}'.format(year, format(month, '02d'), scrubbedName)
                        l = Link(format = contentFormat,
                                 URI = uri,
                                 contentItem = confTalk)
                        l.save()
                        '''
                    except:
                        continue

    def getResponseJson(self, request):
        response = urllib2.urlopen(request).read()
        return json.loads(response)

if __name__ == "__main__":
    importer = Importer()
    try:
        importer.run()
    except KeyboardInterrupt:
        pass