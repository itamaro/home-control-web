import logging
import json
import urllib
import urllib2

from django.core.urlresolvers import reverse

logger = logging.getLogger(__name__)

def update_url_qs(url, **kwargs):
    qs_dict = dict()
    for k, v in kwargs.iteritems():
        if v:
            qs_dict[k] = v
    if qs_dict:
        u, qs = urllib.splitquery(url)
        qs = '&'.join((qs and qs or '', urllib.urlencode(qs_dict)))
        return '%s?%s' % (u, qs)
    return url

def silly_reverse(request, lookup_view, *args, **kwargs):
    "Append ?key=<key> query string to generated view-URL"
    the_url = reverse(lookup_view, args=args, kwargs=kwargs)
    key = getattr(request, 'silly_auth_pass', None)
    return update_url_qs(the_url, key=key)

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
