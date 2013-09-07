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
    return render(request, 'ac.html', d)

def command(request):
    _checkauth(request)
    try:
        res = urllib.urlopen(HOME_CONTROL_ACCMD_RPC_URL).read()
    except IOError, ex:
        logger.error('Failed Arduino RPC: %s' % (ex))
        res = 'No Response'
    return HttpResponse(res)
