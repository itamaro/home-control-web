# Create your views here.
import urllib
import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import PermissionDenied

# The secret key for accessing the home control interface - default is empty
HOME_CONTROL_SECRET_KEY = getattr(settings, 'HOME_CONTROL_SECRET_KEY', '')

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
    d['thingie'] = request.META.items() # [(var, val) for var, val in request.META.iteritems()]
    return render(request, 'debug/debug.html', d)
