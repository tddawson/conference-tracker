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
        self.importGeneralConference()

    def importGeneralConference(self):
        logging.info("Importing General Conference")

        conferenceListEndpoint = 'https://tech.lds.org/mc/api/conference/list'
        logging.debug("Requesting {}".format(conferenceListEndpoint))
        req = urllib2.Request(url=conferenceListEndpoint, data='LanguageID=1')
        conferenceList = self.getResponseJson(req)

        Conferences = conferenceList['Conferences']
        try:
            GeneralConferenceFolder = Folder.objects.get(name = "General Conference")
        except:
            GeneralConferenceFolder = Folder(name = "General Conference")
            GeneralConferenceFolder.save()

        for conference in Conferences:
            self.importConference(conference, GeneralConferenceFolder)

    def importConference(self, conference, generalConferenceFolder):
        logging.info(conference['Title'])
        try:
            generalConferenceFolder = Folder.objects.get(name= conference['Title'])
            logging.info("Session Already Imported")
            return
        except:
            individualConferenceFolder = Folder(name = conference['Title'], parentFolder = generalConferenceFolder)
            individualConferenceFolder.save()

        sessionListEndpoint = 'http://tech.lds.org/mc/api/conference/sessionlist'
        req = urllib2.Request(url = sessionListEndpoint,
                                data = 'ConferenceID='+str(conference['ID']))

        Sessions = self.getResponseJson(req)['Sessions']

        for session in Sessions:
            self.importSession(session, individualConferenceFolder)

    def importSession(self, session, conferenceFolder):
        SessionFolder = Folder(name = session['Title'], parentFolder = conferenceFolder)

        SessionFolder.save()

        req = urllib2.Request(url = 'http://tech.lds.org/mc/api/conference/talklist',
                                data = 'SessionID='+str(session['ID']))

        talkList = self.getResponseJson(req)
        Talks = talkList['Talks']

        for talk in Talks:
            self.importTalk(talk, SessionFolder)

    def importTalk(self, talk, sessionFolder):
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
                    return
                else:
                    a = Author(name = authorName)
                    a.save()


            confTalk = ConferenceTalk(title = talk['Title'],
                                     folder = sessionFolder,
                                     author = a)

            confTalk.save()

            for link in talk['Media']:
                self.importLink(link, confTalk)

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
            return

    def importLink(self, link, confTalk):
        try:
            contentFormat = ContentFormat.objects.get(container = link['MediaContainer'])
        except:
            contentFormat = ContentFormat(  type = link['MediaType'],
                                            container = link['MediaContainer'])
            contentFormat.save()

        l = Link(format = contentFormat,
                 URI = link['URL'],
                 contentItem = confTalk)
        l.save()

    def getResponseJson(self, request):
        response = urllib2.urlopen(request).read()
        return json.loads(response)

if __name__ == "__main__":
    importer = Importer()
    try:
        importer.run()
    except KeyboardInterrupt:
        pass