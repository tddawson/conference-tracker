from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length = 200)
	email = models.CharField(max_length = 200)

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
	user = models.ForeignKey(User)
	dateCompleted = models.DateTimeField('Date Completed')
	content = models.OneToOneField(ContentItem)


	
	
