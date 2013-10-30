import urllib
import logging
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from AC.models import AcControl

logger = logging.getLogger(__name__)

def navbar_item():
    "Return (lookup_view, nav_text) tuple for current app"
    return ('AC-home', 'A/C')

def home(request):
    return TemplateResponse(request, 'AC/ac.html', {
            'inst_objects': AcControl.objects.all(),
        })

def control_form(request, ac_id):
    "Render A/C control form for selected A/C"
    ac = get_object_or_404(AcControl, pk=ac_id)
    return TemplateResponse(request, 'AC/ac.html', {
            'inst_objects': AcControl.objects.all(),
            'active_inst': ac,
        })

def command(request, ac_id):
    "Send A/C command to selected A/C and return result"
    ac = get_object_or_404(AcControl, pk=ac_id)
    res = ac.command(request.GET)
    return HttpResponse(json.dumps(res), content_type='applicatoin/json')
