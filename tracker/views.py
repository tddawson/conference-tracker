from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from tracker.models import *
from datetime import datetime 
import sys

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

def conference_talks_by_session(request, session):
	talks = ConferenceTalk.objects.filter(folder__parentFolder__name=session)

	context = {'talks': talks, 'folder': session}
	return render(request, 'tracker/choose_talk.html', context)

def conference_talks_by_speaker(request, speaker):
	talks = ConferenceTalk.objects.filter(author__name=speaker)

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		pk = user.pk
	completed_items = Completion.objects.filter(user__pk=pk)
	pks = [item.content.pk for item in completed_items]

	context = {'talks': talks, 'folder': speaker, 'pks': pks,  'user': user}
	return render(request, 'tracker/choose_talk.html', context)


def conference_talks_by_topic(request, topic):
	talks = ConferenceTalk.objects.filter(tags__name__in=[topic])

	context = {'talks': talks, 'folder': topic}
	return render(request, 'tracker/choose_talk.html', context)


def conference_talk(request, talk):
	talk = ConferenceTalk.objects.filter(title=talk)[0]

	context = {'talk': talk}
	return render(request, 'tracker/talk.html', context)


def mark_complete(request, content_id):
	try: 
		if request.user.is_authenticated():
			user = User.objects.get(pk=request.user.id)
		else:
			return HttpResponse("You are not logged in!")
		date = datetime.now()
		talk = ConferenceTalk.objects.get(pk=content_id)

		if len(Completion.objects.filter(user=user, content=talk)) > 0:
			#Already saved... we'll allow it for now.
			return HttpResponse("Success")

		completion = Completion(user=user, dateCompleted=date, content=talk)
		completion.save()
	except:
		e = sys.exc_info()[0]
		return HttpResponse(e)

	return HttpResponse("Success")

def profile(request):
	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		return HttpResponse("You logged in as: %s" % (user))
	else:
		return HttpResponse("You failed to log in... Sorry!")
