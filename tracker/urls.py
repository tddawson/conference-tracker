from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
    url(r'^home/', views.home, name='home'),
    url(r'^general-conference/sessions/$', views.conference_sessions, name='conference_sessions'),
    url(r'^general-conference/speakers/', views.conference_speakers, name='conference_speakers'),
    url(r'^general-conference/topics/', views.conference_topics, name='conference_topics'),
)