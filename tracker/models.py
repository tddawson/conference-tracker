from django.contrib.auth.models import User
from django.db import models

#AUTH_USER_MODEL = 'django_facebook.FacebookCustomUser'

class Author(models.Model):
	name = models.CharField(max_length = 200)

	def __unicode__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length = 200)

	def __unicode__(self):
		return self.name


class Folder(models.Model):
	name = models.CharField(max_length =200) 
	parentFolder = models.ForeignKey('Folder', null = True, blank = True)

	def __unicode__(self):
		return self.name


class ContentItem(models.Model):
	#title = models.CharField(max_length = 200)
	#author = models.ForeignKey(Author)
	folder = models.ForeignKey(Folder)
	tags = models.ManyToManyField(Tag)


class Link(models.Model):
	type = models.CharField(max_length = 10)
	URI = models.CharField(max_length = 200)
	contentItem = models.ForeignKey(ContentItem)

	def __unicode__(self):
		return self.uri

class ConferenceTalk(ContentItem):
	title = models.CharField(max_length = 200)
	author = models.ForeignKey(Author)

	def __unicode__(self):
		return self.title

class Completion(models.Model):
	user = models.ForeignKey(User)
	dateCompleted = models.DateTimeField('Date Completed')
	content = models.OneToOneField(ContentItem)
