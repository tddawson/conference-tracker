from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
    url(r'^home/', views.home, name='home'),
    url(r'^explore(?P<sort_by>)/$', views.explore, name='explore'),
    url(r'^explore/(?P<sort_by>\w+)/', views.explore, name='explore'),
)