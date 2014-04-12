from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
    url(r'^home/', views.home, name='home'),
    url(r'^complete/(?P<content_id>\d+)/$', views.mark_complete, name='mark_complete'),
    url(r'^general-conference/$', views.conference_sessions, name='conference_sessions'),
    url(r'^general-conference/sessions/$', views.conference_sessions, name='conference_sessions'),
    url(r'^general-conference/sessions/(?P<session>[\w\s]+)/$', views.conference_talks_by_session, name='conference_talks_by_session'),
    url(r'^general-conference/speakers/$', views.conference_speakers, name='conference_speakers'),
    url(r'^general-conference/speakers/(?P<speaker>[\w\.\s]+)/$', views.conference_talks_by_speaker, name='conference_talks_by_speaker'),
    url(r'^general-conference/topics/$', views.conference_topics, name='conference_topics'),
    url(r'^general-conference/topics/(?P<topic>[\w\.\s]+)/$', views.conference_talks_by_topic, name='conference_talks_by_topic'),
    url(r'^general-conference/talks/(?P<talk>[\w\.\s\-]+)/$', views.conference_talk, name='conference_talk'),
)