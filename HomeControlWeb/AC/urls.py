from django.conf.urls import patterns, url

from AC import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='AC-home'),
    url(r'^(?P<ac_id>\d+)/$', views.control_form, name='AC-control-form'),
    url(r'^(?P<ac_id>\d+)/command/$', views.command, name='AC-command'),
)
