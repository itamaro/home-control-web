import urllib

from django import template

from .. import silly_reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def silly_url(context, lookup_view, *args, **kwargs):
    "Append ?key=<key> query string to generated view-URL"
    return silly_reverse(context['request'], lookup_view, *args, **kwargs)
