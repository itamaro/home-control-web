import logging
from django.template.response import TemplateResponse
from django.conf import settings

import common
import common.views

logger = logging.getLogger(__name__)

def navbar_item():
    "Return (lookup_view, nav_text) tuple for current app"
    return ('debug-home', 'Debug')

def home(request):
    return TemplateResponse(request, 'debug/debug.html',
                            {'req_meta': request.META.items()})
