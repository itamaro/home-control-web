from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^AC/', include('AC.urls')),
    url(r'^cam/', include('cam.urls')),
    url(r'^debug/', include('debug.urls')),
)
