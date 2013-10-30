from django.conf.urls import patterns, url

from cam import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='cam-home'),
    url(r'^(?P<cam_id>\d+)/$', views.webcam, name='webcam'),
    url(r'^(?P<cam_id>\d+)/snapshot/$', views.snapshot, name='cam-snapshot'),
)
