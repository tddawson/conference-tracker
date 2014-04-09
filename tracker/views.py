from django.shortcuts import render

from tracker.models import SiteUser
from tracker.models import Author
from tracker.models import Tag
from tracker.models import Folder
from tracker.models import ContentItem
from tracker.models import Link
from tracker.models import Author
from tracker.models import ConferenceTalk
from tracker.models import Completion

def home(request):
	sample_list = ["one", "two", "three"]
	context = {'var_name': sample_list}
	return render(request, 'tracker/home.html', context)


def conference_sessions(request):
	sessions = Folder.objects.filter(parentFolder__name='General Conference')

	context = {'categories': sessions, "sort_by": "session"}
	return render(request, 'tracker/explore_conference.html', context)


def conference_speakers(request):
	speakers = Author.objects.all()

	context = {'categories': speakers, "sort_by": "speaker"}
	return render(request, 'tracker/explore_conference.html', context)


def conference_topics(request):
	topics = Tag.objects.all()

	context = {'categories': topics, "sort_by": "topic"}
	return render(request, 'tracker/explore_conference.html', context)

