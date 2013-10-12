import logging
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
