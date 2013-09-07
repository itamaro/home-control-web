from django.conf.urls import patterns, url

from cam import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^webcam$', views.webcam, name='webcam'),
    url(r'^webcam.png$', views.webcam_proxy_png, name='webcam_proxy_png'),
)
