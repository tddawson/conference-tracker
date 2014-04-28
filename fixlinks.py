# This should be a one-time fix to the LDS.org links

#Set up the Django enviornment and import the data models
import urllib2
import json
import logging
import sys

import sys, os
sys.path.append('app/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from tracker.models import *


class LinkFixer:

	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')

	def run(self):
		talks = ConferenceTalk.objects.all()
	
		for talk in talks:
	
			# Set the simple title to the new version of improved title.
			talk.simpleTitle = talk.getSimpleTitle()
			talk.save()

			# Set the LDS read link to the correct link.
			links = talk.link_set.all()
			for link in links:
				if link.format.type != 'Video' and link.format.type != 'Audio':
					urlPostfix = talk.getUrlPostfix()
					uri = 'http://www.lds.org/general-conference/' + urlPostfix
					link.URI = uri
					link.save()
	


if __name__ == "__main__":
    fixer = LinkFixer()
    try:
        fixer.run()
    except KeyboardInterrupt:
        pass