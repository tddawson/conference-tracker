from django.contrib.auth.models import User
from django.db import models

AUTH_USER_MODEL = 'django_facebook.FacebookCustomUser'

# SiteUser instead of User because Django's auth system already has a notion of User
class SiteUser(models.Model):
	user = models.OneToOneField(User)
	# Now we can extend their User (which houses basic username, password, email, etc)

class Author(models.Model):
	name = models.CharField(max_length = 200)

class Tag(models.Model):
	name = models.CharField(max_length = 200)

class Folder(models.Model):
	name = models.CharField(max_length =200) 

class ContentItem(models.Model):
	title = models.CharField(max_length = 200)
	author = models.ForeignKey(Author)
	folder = models.ForeignKey(Folder)
	tags = models.ManyToManyField(Tag)

class ContentURI(models.Model):
	URI = models.CharField(max_length = 200)
	contentType = models.CharField(max_length = 10)
	contentItem = models.ForeignKey(ContentItem)

class Completion(models.Model):
	user = models.ForeignKey(SiteUser)
	dateCompleted = models.DateTimeField('Date Completed')
	content = models.OneToOneField(ContentItem)



