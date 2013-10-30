from django.conf.urls import patterns, url

from ESXi import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='rhosts-home'),
    url(r'^(?P<host_id>\d+)/$', views.host_data_from_cache, name='rhost-cached-data'),
    url(r'^update-remote-data/(?P<host_id>\d+)/$', views.update_remote_host_data, name='rhost-update-remote-data'),
    url(r'^turn-on/vm/(?P<vm_id>\d+)/$', views.turn_on_vm, name='rhost-turn-on-vm'),
    url(r'^shutdown/vm/(?P<vm_id>\d+)/$', views.shutdown_vm, name='rhost-shutdown-vm'),
    url(r'^get-data/vm/(?P<vm_id>\d+)/$', views.get_vm_data_from_cache, name='rhost-get-cache-vm-data'),
    url(r'^shutdown/host/(?P<host_id>\d+)/$', views.shutdown_host, name='rhost-shutdown-host'),
    url(r'^turn-on/host/(?P<host_id>\d+)/$', views.turn_on_host, name='rhost-turn-on-host'),
)
