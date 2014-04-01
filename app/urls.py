from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Django's default admin tools
    url(r'^admin/', include(admin.site.urls)),

    # Pass main control over to the tracker views
    url(r'^', include('tracker.urls')),
)
