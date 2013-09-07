from django.conf.urls import patterns, url

from AC import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^command$', views.command, name='command'),
)
