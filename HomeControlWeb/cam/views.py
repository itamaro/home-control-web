# Create your views here.
import urllib
import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import PermissionDenied

# The secret key for accessing the home control interface - default is empty
HOME_CONTROL_SECRET_KEY = getattr(settings, 'HOME_CONTROL_SECRET_KEY', '')
HOME_CONTROL_WEBCAM_RPC_URL = getattr(settings, 'HOME_CONTROL_WEBCAM_RPC_URL',
                                'http://localhost:8000/webcam.png')
# A local path where the webcam image will be stored
# The user running the server process will need write access to this path,
# so choose it wisely...
HOME_CONTROL_LOCAL_WEBCAM_IMAGE_PATH = getattr(settings,
                                'HOME_CONTROL_LOCAL_WEBCAM_IMAGE_PATH',
                                '/var/www/static/img/webcam/webcam-image.png')
# The URL mapping for serving the webcam image
HOME_CONTROL_WEBCAM_IMAGE_URL = getattr(settings,
                                'HOME_CONTROL_WEBCAM_IMAGE_URL',
                                '/static/img/webcam/webcam-image.png')

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
    return render(request, 'cam.html', d)

def webcam(request):
    _checkauth(request)
    try:
        urllib.urlretrieve(HOME_CONTROL_WEBCAM_RPC_URL,
                           HOME_CONTROL_LOCAL_WEBCAM_IMAGE_PATH)
        res = '<img src="%s" />' % (HOME_CONTROL_WEBCAM_IMAGE_URL)
    except IOError, ex:
        logger.error('Failed WebCam RPC: %s' % (ex))
        res = 'Failed Retrieving Image'
    return HttpResponse(res)

    return HttpResponse('WebCam stub')

def webcam_proxy_png(request):
    _checkauth(request)
    return HttpResponse(urllib.urlopen(HOME_CONTROL_WEBCAM_RPC_URL).read(),
                        mimetype='image/png')
