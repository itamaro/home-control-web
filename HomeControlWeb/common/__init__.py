import logging
import json
import urllib
import urllib2

from django.conf import settings
from django.core.exceptions import PermissionDenied

# The secret key for accessing the home control interface - default is empty
HOME_CONTROL_SECRET_KEY = getattr(settings, 'HOME_CONTROL_SECRET_KEY', '')

logger = logging.getLogger(__name__)

def checkpass(request):
    key = request.GET.get('key', '')
    if key != HOME_CONTROL_SECRET_KEY:
        raise PermissionDenied()
    return {'key': request.GET.get('key', None)}

def load_json_from_url(*args, **kwargs):
    "Loads and returns a JSON object obtained from a URL specified by the " \
    "positional arguments with query-string generated from keyword arguments"
    url = '/'.join(args)
    scheme, url = urllib2.splittype(url)
    url = url.strip('/') + '/'
    while '//' in url:
        url = url.replace('//', '/')
    url_req = '://'.join((scheme, url))
    if kwargs:
        url_req += '?' + urllib.urlencode(kwargs)
    req = urllib2.Request(url_req)
    opener = urllib2.build_opener()
    return json.load(opener.open(req))
