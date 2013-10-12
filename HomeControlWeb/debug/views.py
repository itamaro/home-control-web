# Create your views here.
import logging
from django.shortcuts import render
from django.conf import settings

import common

logger = logging.getLogger(__name__)

def home(request):
    d = common.checkpass(request)
    d['req_meta'] = request.META.items()
    return render(request, 'debug/debug.html', d)
