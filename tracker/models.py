from django.contrib.auth.models import User
from django.db import models
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
    parentFolder = models.ForeignKey('Folder', null=True, blank=True)

    def __unicode__(self):
        return self.name

class ContentItem(models.Model):
    #title = models.CharField(max_length = 200)
    #author = models.ForeignKey(Author)
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

class ConferenceTalk(ContentItem):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author)

    def __unicode__(self):
        return self.title

    def simpleTitle(self):
        simpleTitle = re.sub('[\s]', '-', self.title)
        simpleTitle = re.sub('[^\w-]', '', simpleTitle)
        print self.title
        return simpleTitle

    def smallLinks(self):
        return self.link_set.filter(~Q(format__container='YouTube'))

    def youTubeEmbedLink(self):
        link = self.link_set.filter(format__container='YouTube').first().URI
        uniqueId = link.split("=")[1]
        embedLink = '//www.youtube.com/embed/' + uniqueId
        return embedLink

class Completion(models.Model):
    user = models.ForeignKey(User)
    dateCompleted = models.DateTimeField('Date Completed')
    content = models.OneToOneField(ContentItem)
