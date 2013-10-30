import logging
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from ESXi.models import EsxiHost, VirtualMachine

logger = logging.getLogger(__name__)

def navbar_item():
    "Return (lookup_view, nav_text) tuple for current app"
    return ('rhosts-home', 'Remote Hosts')
    
def home(request):
    return TemplateResponse(request, 'ESXi/esxi.html', {
            'inst_objects': EsxiHost.objects.all(),
        })

def host_data_from_cache(request, host_id):
    "Renders host data from local cache"
    host = get_object_or_404(EsxiHost, pk=host_id)
    return TemplateResponse(request, 'ESXi/esxi.html', {
            'inst_objects': EsxiHost.objects.all(),
            'active_inst': host,
        })

def get_vm_data_from_cache(request, vm_id):
    "Renders VM data from local cache"
    vm = get_object_or_404(VirtualMachine, pk=vm_id)
    return HttpResponse(json.dumps({'power': vm.power_state}),
                        content_type='application/json')

def update_remote_host_data(request, host_id):
    "Update local cache from remote host"
    host = get_object_or_404(EsxiHost, pk=host_id)
    host.update_from_rpc()
    return HttpResponse('ACK')

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
