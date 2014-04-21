#Set up the Django enviornment and import the data models
import urllib2
import json
import logging
import sys

import sys, os
sys.path.append('app/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from tracker.models import *

class Importer:

    def __init__(self):
        logging.basicConfig(filename='importer.log', level=logging.INFO)
        self.authorsToSkip = ["presented by", "afternoon", "morning", "choir", "priesthood", "congregation", "meeting"]
        self.namePrefixes = ["president", "elder", "sister", "brother", "bishop"]

        reload(sys)
        sys.setdefaultencoding('utf-8')

    def run(self):
        self.importGeneralConference()

    def importGeneralConference(self):
        logging.info('-------------------------------------------------')
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

        logging.info("General Conference import complete!")

    def importConference(self, conference, generalConferenceFolder):
        conferenceTitle = conference['Title'].split(',')[0]
        year = conference['Year']
        month = conference['Month']
        logging.info('-------------------------------------------------')
        logging.info(conferenceTitle)

        try:
            generalConferenceFolder = Folder.objects.get(name = conferenceTitle)
            logging.info("Session Already Imported")
            return
        except:
            individualConferenceFolder = Conference(name = conferenceTitle, parentFolder = generalConferenceFolder,
                                                    year = year, month = month)
            individualConferenceFolder.simpleName = individualConferenceFolder.getSimpleName()
            individualConferenceFolder.save()

        sessionListEndpoint = 'http://tech.lds.org/mc/api/conference/sessionlist'
        req = urllib2.Request(url = sessionListEndpoint,
                                data = 'ConferenceID='+str(conference['ID']))

        Sessions = self.getResponseJson(req)['Sessions']

        for session in Sessions:
            self.importSession(session, individualConferenceFolder)

    def importSession(self, session, conferenceFolder):
        sessionTitle = session['Title']
        logging.info(sessionTitle)

        SessionFolder = Folder(name = sessionTitle, parentFolder = conferenceFolder)

        SessionFolder.save()

        req = urllib2.Request(url = 'http://tech.lds.org/mc/api/conference/talklist',
                                data = 'SessionID='+str(session['ID']))

        talkList = self.getResponseJson(req)
        Talks = talkList['Talks']

        for talk in Talks:
            self.importTalk(talk, SessionFolder)

    def importTalk(self, talk, sessionFolder):
        try:
            talkTitle = talk['Title']
            persons = talk['Persons']

            if len(persons) == 0:
                logging.info("Skipping '{}'".format(talkTitle))
                return

            authorName = persons[0]['Name']
            names = authorName.split(' ', 1)

            logging.info( '{} - {}'.format(authorName, talkTitle) )

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
                    logging.info("Skipping '{}'".format(talkTitle))
                    return
                else:
                    a = Author(name = authorName)
                    a.save()

            confTalk = ConferenceTalk(title = talkTitle,
                                      folder = sessionFolder,
                                      author = a)
            confTalk.simpleTitle = confTalk.getSimpleTitle()

            confTalk.save()

            for link in talk['Media']:
                self.importLink(link, confTalk)
            
            self.generateTextUrl(confTalk)

        except Exception as e:
            logging.error(e)

    def importLink(self, link, confTalk):
        container = link['MediaContainer']
        type = link['MediaType']
        url = link['URL']
        logging.debug('LINK: {}:{}:{}'.format(container, type, url))

        try:
            contentFormat = ContentFormat.objects.get(container = container)
        except:
            contentFormat = ContentFormat(  type = type,
                                            container = container)
            contentFormat.save()

        l = Link(format = contentFormat,
                 URI = url,
                 contentItem = confTalk)
        l.save()

    def generateTextUrl(self, talk):
        try:
            contentFormat = ContentFormat.objects.get(container = 'LDS.org')
        except:
            contentFormat = ContentFormat(  type = 'Text',
                                            container = 'LDS.org')
            contentFormat.save()

        urlPostfix = talk.getUrlPostfix()
        uri = 'https://www.lds.org/general-conference/' + urlPostfix
        l = Link(format = contentFormat,
                 URI = uri,
                 contentItem = talk)
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