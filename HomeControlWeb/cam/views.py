import logging
import json
import urllib

from django.http import HttpResponse
from django.template.response import TemplateResponse

from cam.models import WebCamProxy

logger = logging.getLogger(__name__)

def navbar_item():
    "Return (lookup_view, nav_text) tuple for current app"
    return ('cam-home', 'Webcams')

def home(request):
    return TemplateResponse(request, 'cam/cam.html')

def webcam(request):
    res = {u'status': u'ERROR', u'msg': u'Failed Retrieving Image'}
    # TODO: fix object selection
    try:
        cam = WebCamProxy.objects.all()[0]
        snapshot_url = cam.get_snapshot()
        if snapshot_url:
            key = getattr(request, 'silly_auth_pass', None)
            if key:
                snapshot_url = '%s?%s' % (snapshot_url,
                                          urllib.urlencode({'key': key}))
            res = {u'status': u'SUCCESS', u'image-src': snapshot_url}
    except Exception, ex:
        logger.error('Error in get_snapshot: %s', ex)
    return HttpResponse(json.dumps(res), content_type='application/json')
