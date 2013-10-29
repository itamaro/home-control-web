import importlib

from django.conf import settings
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.core.exceptions import MiddlewareNotUsed

class NavbarMiddleware(object):
    def __init__(self):
        self._navbar_apps = list(getattr(settings, 'NAVBAR_APPS', None))
        if self._navbar_apps is None:
            raise MiddlewareNotUsed()

    def process_template_response(self, request, response):
        "Add navbar elements to response context data"
        if not response.context_data:
            response.context_data = dict()
        response.context_data['navbar_apps'] = list()
        for app in self._navbar_apps:
            if not app in settings.INSTALLED_APPS:
                # Skip inactive app
                continue
            try:
                app_views = importlib.import_module('%s.views' % (app))
                if hasattr(app_views, 'navbar_item'):
                    response.context_data['navbar_apps'].append(
                                                    app_views.navbar_item())
            except ImportError:
                pass
        return response
