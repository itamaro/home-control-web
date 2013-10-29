from django.conf.urls import patterns, url

from AC import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='AC-home'),
    url(r'^command$', views.command, name='ac-command'),
)
