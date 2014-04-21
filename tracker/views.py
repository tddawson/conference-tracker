from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from tracker.models import *
from datetime import datetime 
import sys
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout as auth_logout

def home(request):
	talks = mostPopularItems()
	

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		# Get 5 most recently completed items
		completed_items = Completion.objects.filter(user__pk=user.pk).order_by('pk').reverse()[:5]
		num_completed_talks = len(Completion.objects.filter(user__pk=user.pk))
		num_total_talks = len(ConferenceTalk.objects.all())
		context = {"user":user, "completed_items":completed_items, "most_popular":talks, "num_completed_talks":num_completed_talks, "num_total_talks":num_total_talks}

		return render(request, 'tracker/home_logged_in.html', context)
	else:
		return render(request, 'tracker/home.html', {"most_popular":talks})


def conference_sessions(request):
	sessions = Conference.objects.filter(parentFolder__name='General Conference')

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		for session in sessions:
			talks_in_session = ConferenceTalk.objects.filter(folder__parentFolder__name=session)
			session.num_total = len(talks_in_session)
			session.num_completed = len(Completion.objects.filter(user=user, content__in=talks_in_session))
			month_num = session.month
			if month_num == 10:
				month = "October"
			else:
				month = "April"
			session.display_name = "%s %d" % (month, session.year)

	context = {'categories': sessions, "sort_by": "session"}
	return render(request, 'tracker/explore_conference.html', context)


def conference_speakers(request):
	speakers = Author.objects.all()

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		for speaker in speakers:
			talks_by_speaker = ConferenceTalk.objects.filter(author__name=speaker)
			speaker.num_total = len(talks_by_speaker)
			speaker.num_completed = len(Completion.objects.filter(user=user, content__in=talks_by_speaker))


	context = {'categories': speakers, "sort_by": "speaker"}
	return render(request, 'tracker/explore_conference.html', context)


def conference_topics(request):
	topics = Tag.objects.all()

	context = {'categories': topics, "sort_by": "topic"}
	return render(request, 'tracker/explore_conference.html', context)

def conference_talks_by_session(request, session):
	talks = ConferenceTalk.objects.filter(folder__parentFolder__name=session)


	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		pk = user.pk
		completed_items = Completion.objects.filter(user__pk=pk)
		pks = [item.content.pk for item in completed_items]
	else:
		pks = []
		user = User()
		month = Conference.objects.filter(name=session)[0].month #session.parentFolder.month
		

	context = {'talks': talks, 'folder': session, 'pks': pks, 'user': user}
	return render(request, 'tracker/choose_talk.html', context)

def conference_talks_by_speaker(request, speaker):
	talks = ConferenceTalk.objects.filter(author__name=speaker)

	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		pk = user.pk
		completed_items = Completion.objects.filter(user__pk=pk)
		pks = [item.content.pk for item in completed_items]
	else:
		pks = []
		user = User()


	context = {'talks': talks, 'folder': speaker, 'pks': pks,  'user': user}
	return render(request, 'tracker/choose_talk.html', context)


def conference_talks_by_topic(request, topic):
	talks = ConferenceTalk.objects.filter(tags__name__in=[topic])

	context = {'talks': talks, 'folder': topic}
	return render(request, 'tracker/choose_talk.html', context)


def conference_talk(request, year, month, talk):
	conference = Conference.objects.get(year=year, month=month)
	talk = ConferenceTalk.objects.filter(simpleTitle=talk, folder__parentFolder__pk=conference.pk)[0]
	more_from_session = ConferenceTalk.objects.filter(folder__parentFolder__name=talk.folder.parentFolder).exclude(simpleTitle=talk.simpleTitle)[:5]

	more_by_speaker = ConferenceTalk.objects.filter(author=talk.author).exclude(simpleTitle=talk.simpleTitle)[:5]
	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		completed = len(Completion.objects.filter(user=user, content=talk)) == 1
                pk = user.pk
                completed_items = Completion.objects.filter(user__pk=pk)
                pks = [item.content.pk for item in completed_items]

	else:
		completed = False
		pks = []

	context = {'talk': talk, 'completed': completed, 'more_from_session': more_from_session, 'more_by_speaker': more_by_speaker, 'pks': pks}
	return render(request, 'tracker/talk.html', context)


def mark_complete(request, content_id):
	try: 
		if request.user.is_authenticated():
			user = User.objects.get(pk=request.user.id)
		else:
			return HttpResponse("You are not logged in!")
		date = datetime.now()
		talk = ConferenceTalk.objects.get(pk=content_id)

		if len(Completion.objects.filter(user=user, content=talk)) == 1:
			#Already saved, mark as incomplete.
			c = Completion.objects.get(user=user, content=talk)
			c.delete()
			return HttpResponse("Deleted")
		
		# No completed item recorded, save it!
		completion = Completion(user=user, dateCompleted=date, content=talk)
		
		completion.save()
	except:
		e = sys.exc_info()[0]
		return HttpResponse(e)

	return HttpResponse("Added")

def profile(request):
	"""After logging in"""
	return render(request, 'tracker/home.html', {})
	
	"""Should display differently depending on if they are logged in."""
	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.id)
		return HttpResponse("You logged in as: %s" % (user))
	else:
		return HttpResponse("You failed to log in... Sorry!")


def logout(request):
	"""Logs out user"""
	auth_logout(request)
	return render_to_response('tracker/logout.html', {'dont_redirect':True}, RequestContext(request))
