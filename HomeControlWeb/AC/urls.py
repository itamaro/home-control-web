from django.conf.urls import patterns, url

from AC import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^webcam$', views.webcam, name='webcam'),
    url(r'^webcam.png$', views.webcam_proxy_png, name='webcam_proxy_png'),
    url(r'^command$', views.command, name='command'),
)
