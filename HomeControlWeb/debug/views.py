# Create your views here.
import logging
from django.shortcuts import render
from django.conf import settings

import common
import common.views

logger = logging.getLogger(__name__)

def get_nav_name():
    return 'Debug'

def home(request):
    d = common.checkpass(request)
    d = common.views.get_nav_elements(d)
    d['req_meta'] = request.META.items()
    return render(request, 'debug/debug.html', d)
