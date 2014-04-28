from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.db.models import Q
import re


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Folder(models.Model):
    name = models.CharField(max_length=200)
    simpleName = models.CharField(max_length=200)
    parentFolder = models.ForeignKey('Folder', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def getSimpleName(self):
        simpleName = re.sub('[\s]', '-', self.name)
        simpleName = re.sub('[^\w-]', '', simpleName)
        return simpleName

class ContentItem(models.Model):
    folder = models.ForeignKey(Folder)
    tags = models.ManyToManyField(Tag)

class ContentFormat(models.Model):
    type = models.CharField(max_length=10)
    container = models.CharField(max_length=10)

    def __unicode__(self):
        return self.container

class Link(models.Model):
    format = models.ForeignKey(ContentFormat)
    URI = models.CharField(max_length=200)
    contentItem = models.ForeignKey(ContentItem)

    def __unicode__(self):
        return self.URI

    def action(self):
        if(self.format.type == 'Video'):
            action = 'Watch'
        elif(self.format.type == 'Audio'):
            action = 'Listen'
        else:
            action = 'Read'

        if(self.format != ''):
            action = action + ' ({})'.format(self.format)

        return action

class Conference(Folder):
    year = models.IntegerField()
    month = models.IntegerField()

    def twoDigitMonth(self):
        if self.month == 4:
            return "04"
        return "10"

    def getFullDate(self):
        if self.month == 4:
            return "April %d" % (self.year)
        return "October %d" % (self.year)
        

class ConferenceTalk(ContentItem):
    title = models.CharField(max_length=200)
    simpleTitle = models.CharField(max_length=200)
    author = models.ForeignKey(Author)

    def __unicode__(self):
        return self.title

    def getSimpleTitle(self):
        simpleTitle = re.sub(u'[\s\u2014]', u'-', self.title, re.UNICODE)
        simpleTitle = re.sub(u'[^\w\-\u2014]', u'', simpleTitle, re.UNICODE)
        return simpleTitle

    def getUrlPostfix(self):
        conference = self.getConference()
        urlPostfix = "{}/{}/{}".format(conference.year, conference.twoDigitMonth(), self.getSimpleTitle())
        return urlPostfix

    def getConference(self):
        conference = Conference.objects.get(folder_ptr_id=self.folder.parentFolder.pk)
        return conference

    def smallLinks(self):
        return self.link_set.filter(~Q(format__container='YouTube'))

    def youTubeEmbedLink(self):
        link = self.link_set.filter(format__container='YouTube').first().URI
        uniqueId = link.split("=")[1]
        embedLink = '//www.youtube.com/embed/' + uniqueId
        return embedLink

    def hasYouTubeLink(self):
        if len(self.link_set.filter(format__container='YouTube')) >= 1:
            return True
        return False

class Completion(models.Model):
    user = models.ForeignKey(User)
    dateCompleted = models.DateTimeField('Date Completed')
    content = models.ForeignKey(ContentItem)


def mostPopularItems():
    ids = Completion.objects.values('content').annotate(c=Count('content')).order_by('-c')[:5]
    talks = []
    for id in ids:
        talks.append(ConferenceTalk.objects.get(pk=id['content']))
    return talks
 

