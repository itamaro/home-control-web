from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.exceptions import MiddlewareNotUsed

class SillyAuthMiddleware(object):
    def __init__(self):
        # The secret key for accessing the Silly Auth protected sites
        #  (default is disabled)
        self._pass = getattr(settings, 'SILLY_AUTH_PASS', None)
        if self._pass is None:
            raise MiddlewareNotUsed()
        self._ignore_paths = set(['/admin/'])

    def process_request(self, request):
        "Verify password for Silly Auth authentication and save it in request"
        for ignored_path in self._ignore_paths:
            if request.path.startswith(ignored_path):
                return
        key = request.GET.get('key', '')
        if key != self._pass:
            raise PermissionDenied()
        request.silly_auth_pass = key
