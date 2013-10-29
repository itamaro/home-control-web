import urllib
import logging
import json

from django.http import HttpResponse
from django.template.response import TemplateResponse

from AC.models import AcControl

logger = logging.getLogger(__name__)

def navbar_item():
    "Return (lookup_view, nav_text) tuple for current app"
    return ('AC-home', 'A/C')

def home(request):
    # TODO: fix object selection
    ac = AcControl.objects.all()[0]
    return TemplateResponse(request, 'AC/ac.html', {'ac': ac})

def command(request):
    # TODO: fix object selection
    ac = AcControl.objects.all()[0]
    res = ac.command(request.GET)
    return HttpResponse(json.dumps(res), content_type='applicatoin/json')
