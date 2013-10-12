# Create your views here.
import urllib
import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import PermissionDenied

# The secret key for accessing the home control interface - default is empty
HOME_CONTROL_SECRET_KEY = getattr(settings, 'HOME_CONTROL_SECRET_KEY', '')
HOME_CONTROL_ACCMD_RPC_URL = getattr(settings, 'HOME_CONTROL_ACCMD_RPC_URL',
                                'http://localhost:8000/ac-command')

logger = logging.getLogger(__name__)

def _checkauth(request):
    key = request.GET.get('key', '')
    if key != HOME_CONTROL_SECRET_KEY:
        raise PermissionDenied()

def home(request):
    _checkauth(request)
    d = dict()
    key = request.GET.get('key', None)
    if key:
        d['key'] = key
    return render(request, 'AC/ac.html', d)

def command(request):
    _checkauth(request)
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
