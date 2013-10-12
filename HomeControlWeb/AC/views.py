# Create your views here.
import urllib
import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

import common

HOME_CONTROL_ACCMD_RPC_URL = getattr(settings, 'HOME_CONTROL_ACCMD_RPC_URL',
                                'http://localhost:8000/ac-command')

logger = logging.getLogger(__name__)

def home(request):
    d = common.checkpass(request)
    return render(request, 'AC/ac.html', d)

def command(request):
    common.checkpass(request)
    ac_params = {
        'mode': request.GET.get('mode'),
        'fan': request.GET.get('fan'),
        'temp': request.GET.get('temp'),
        'pwr': request.GET.get('power'),
    }
    if not all(ac_params.values()):
        # at least one parameter missing
        res = 'Missing Param'
    else:
        try:
            
            res = urllib.urlopen(HOME_CONTROL_ACCMD_RPC_URL + '?' +
                                 urllib.urlencode(ac_params)).read()
        except IOError, ex:
            logger.error('Failed Arduino RPC: %s' % (ex))
            res = 'No Response'
    return HttpResponse(res)
