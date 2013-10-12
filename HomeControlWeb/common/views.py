# Create your views here.
import importlib

from django.conf import settings
from django.core.urlresolvers import reverse

def get_nav_elements(d):
    out = list()
    for app in getattr(settings, 'NAVBAR_APPS_ORDER', ''):
        try:
            app_views = importlib.import_module('%s.views' % (app))
            if hasattr(app_views, 'get_nav_name') and   \
                    hasattr(app_views, 'home'):
                out.append((app_views.get_nav_name(),
                            reverse(app_views.home)))
        except ImportError:
            pass
    if not d:
        d = dict()
    d['nav_elements'] = out
    return d
