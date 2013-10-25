import urllib
import logging
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

import common
import common.views

from AC.models import AcControl

logger = logging.getLogger(__name__)

def get_nav_name():
    return 'A/C'

def home(request):
    d = common.checkpass(request)
    d = common.views.get_nav_elements(d)
    return render(request, 'AC/ac.html', d)

def command(request):
    common.checkpass(request)
    ac = AcControl.objects.all()[0]
    res = ac.command(request.GET)
    return HttpResponse(json.dumps(res), content_type='applicatoin/json')
