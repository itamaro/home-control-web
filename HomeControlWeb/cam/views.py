import logging
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

import common
import common.views

from cam.models import WebCamProxy

logger = logging.getLogger(__name__)

def get_nav_name():
    return 'Cameras'

def home(request):
    d = common.checkpass(request)
    d = common.views.get_nav_elements(d)
    return render(request, 'cam/cam.html', d)

def webcam(request):
    common.checkpass(request)
    # TODO: fix object selection
    cam = WebCamProxy.objects.all()[0]
    if cam.get_snapshot():
        res = {u'status': u'SUCCESS', u'image-src': cam.image_url}
    else:
        res = {u'status': u'ERROR', u'msg': u'Failed Retrieving Image'}
    return HttpResponse(json.dumps(res), content_type='application/json')
