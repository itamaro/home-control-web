from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.exceptions import MiddlewareNotUsed

# The secret key for accessing the Silly Auth protected sites
#  (default is disabled)
SILLY_AUTH_PASS = getattr(settings, 'SILLY_AUTH_PASS', None)

class SillyAuthMiddleware(object):
    def __init__(self):
        if SILLY_AUTH_PASS is None:
            raise MiddlewareNotUsed()

    def process_request(self, request):
        "Verify password for Silly Auth authentication and save it in request"
        key = request.GET.get('key', '')
        if key != SILLY_AUTH_PASS:
            raise PermissionDenied()
        request.silly_auth_pass = key
