import logging
import json
import urllib
import urllib2

from django.core.urlresolvers import reverse

logger = logging.getLogger(__name__)

def silly_reverse(request, lookup_view, *args, **kwargs):
    "Append ?key=<key> query string to generated view-URL"
    the_url = reverse(lookup_view, args=args, kwargs=kwargs)
    key = getattr(request, 'silly_auth_pass', None)
    if key:
        return '%s?%s' % (the_url, urllib.urlencode({'key': key}))
    return the_url

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
