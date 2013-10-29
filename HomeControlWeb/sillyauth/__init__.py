from django.core.urlresolvers import reverse

from common import update_url_qs

def silly_reverse(request, lookup_view, *args, **kwargs):
    "Append ?key=<key> query string to generated view-URL"
    the_url = reverse(lookup_view, args=args, kwargs=kwargs)
    key = getattr(request, 'silly_auth_pass', None)
    return update_url_qs(the_url, key=key)
