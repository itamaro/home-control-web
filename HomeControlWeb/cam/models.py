import logging
import urllib2
import json

from django.db import models

logger = logging.getLogger(__name__)

class WebCamProxy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    rpc_url = models.URLField(default='http://localhost:8000/cam/snapshot/')
    # A local path where the webcam image will be stored
    # The user running the server process will need write access to this path,
    # so choose it wisely...
    local_path = models.CharField(max_length=255,
          default='/var/www/home-control-web/static/img/webcam/snapshot.png')
    # The URL mapping for serving the webcam image
    image_url = models.CharField(max_length=255,
                                 default='/static/img/webcam/snapshot.png')
    
    def __unicode__(self):
        return self.name
    
    def get_snapshot(self):
        u = urllib2.urlopen(self.rpc_url)
        http_msg = u.info()
        res_content_type = http_msg.get('content-type')
        if res_content_type.startswith('image/'):
            # It's an image - save it to local file.
            with open(self.local_path, 'wb') as local_image:
                block_size = 8192
                chunk = True
                while chunk:
                    chunk = u.read(block_size)
                    if chunk:
                        local_image.write(chunk)
            return True
        # Some error. Log it.
        if 'application/json' == res_content_type:
            msg = json.load(u)
        else:
            msg = u.read()
        logger.error('%s failed (%s)' % (self, msg))
        return False
