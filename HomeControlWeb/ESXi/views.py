# Create your views here.
import logging
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.conf import settings

import common
import common.views

from ESXi.models import EsxiHost, VirtualMachine

logger = logging.getLogger(__name__)

def get_nav_name():
    return 'ESXi'
    
def home(request):
    d = common.checkpass(request)
    d = common.views.get_nav_elements(d)
    hosts_list = EsxiHost.objects.order_by('name')
    d['esxi_hosts'] = hosts_list
    return render(request, 'ESXi/esxi.html', d)

def get_host_data_from_cache(request, host_id):
    "Renders host data from local cache"
    d = common.checkpass(request)
    d['host'] = get_object_or_404(EsxiHost, pk=host_id)
    return render(request, 'ESXi/esxi-host-info.html', d)

def get_vm_data_from_cache(request, vm_id):
    "Renders VM data from local cache"
    d = common.checkpass(request)
    vm = get_object_or_404(VirtualMachine, pk=vm_id)
    return HttpResponse(json.dumps({'power': vm.power_state}),
                        content_type='application/json')

def update_remote_host_data(request, host_id):
    "Update local cache from remote ESXi host"
    host = get_object_or_404(EsxiHost, pk=host_id)
    host.update_from_rpc()
    return get_host_data_from_cache(request, host_id)

def turn_on_vm(request, vm_id):
    "Turn on VM on ESXi host"
    vm = get_object_or_404(VirtualMachine, pk=vm_id)
    vm.turn_on()
    return HttpResponse('ACK')

def shutdown_vm(request, vm_id):
    "Shutdown VM on ESXi host"
    vm = get_object_or_404(VirtualMachine, pk=vm_id)
    vm.shutdown()
    return HttpResponse('ACK')

def turn_on_host(request, host_id):
    "Turn on the ESXi host"
    host = get_object_or_404(EsxiHost, pk=host_id)
    host.turn_on()
    return HttpResponse('ACK')
    
def shutdown_host(request, host_id):
    "Shutdown the ESXi host"
    host = get_object_or_404(EsxiHost, pk=host_id)
    host.shutdown()
    return HttpResponse('ACK')
