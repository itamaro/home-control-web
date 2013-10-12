# Create your views here.
import urllib
import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

import common
import common.views

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

def get_nav_name():
    return 'Cameras'

def home(request):
    d = common.checkpass(request)
    d = common.views.get_nav_elements(d)
    return render(request, 'cam/cam.html', d)

def webcam(request):
    common.checkpass(request)
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
    common.checkpass(request)
    return HttpResponse(urllib.urlopen(HOME_CONTROL_WEBCAM_RPC_URL).read(),
                        mimetype='image/png')
