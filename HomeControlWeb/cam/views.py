import logging
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

import common
from cam.models import WebCamProxy

logger = logging.getLogger(__name__)

def navbar_item():
    "Return (lookup_view, nav_text) tuple for current app"
    return ('cam-home', 'Webcams')

def home(request):
    return TemplateResponse(request, 'cam/cam.html', {
            'inst_objects': WebCamProxy.objects.all(),
        })

def webcam(request, cam_id):
    "Render webcam view for selected webcam"
    cam = get_object_or_404(WebCamProxy, pk=cam_id)
    return TemplateResponse(request, 'cam/cam.html', {
            'inst_objects': WebCamProxy.objects.all(),
            'active_inst': cam,
        })

def snapshot(request, cam_id):
    "Send snapshot command and return result"
    res = {u'status': u'ERROR', u'msg': u'Failed Retrieving Image'}
    try:
        cam = WebCamProxy.objects.get(pk=cam_id)
        snapshot_url = cam.get_snapshot()
        if snapshot_url:
            key = getattr(request, 'silly_auth_pass', None)
            snapshot_url = common.update_url_qs(snapshot_url, key=key)
            res = {u'status': u'SUCCESS', u'image-src': snapshot_url}
    except Exception, ex:
        logger.error('Error in get_snapshot: %s', ex)
    return HttpResponse(json.dumps(res), content_type='application/json')
