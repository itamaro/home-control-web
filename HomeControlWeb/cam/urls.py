from django.conf.urls import patterns, url

from cam import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='cam-home'),
    url(r'^webcam/$', views.webcam, name='cam-snapshot'),
)
