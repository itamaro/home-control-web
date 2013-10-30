import urllib

from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def nav_item_active(context, lookup_view):
    "Return 'active' if the `lookup_view` matches the active view"
    return context['request'].path.startswith(reverse(lookup_view)) and     \
           'active' or ''
