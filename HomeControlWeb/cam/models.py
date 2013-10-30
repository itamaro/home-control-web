import os
import logging
import urllib2
import json
from mimetypes import guess_extension

from django.db import models
from django.conf import settings

logger = logging.getLogger(__name__)

class WebCamProxy(models.Model):
    # Webcam name
    name = models.CharField(max_length=100, unique=True)
    # Webcam-RPC URL
    rpc_url = models.URLField(default='http://localhost:8000/cam/snapshot/')
    # Path relative to MEDIA_ROOT to store the webcam snapshot
    # (file name without extension - extension is deduced from mime type)
    # (the web server requires write access to this path)
    snapshot_path = models.CharField(max_length=255,
                                     default='webcam/snapshot')
    
    def __unicode__(self):
        return self.name
    
    def get_snapshot(self):
        "Retrieve webcam snapshot from RPC, save in `snapshot_path`"
        u = urllib2.urlopen(self.rpc_url)
        http_msg = u.info()
        res_content_type = http_msg.get('content-type')
        if res_content_type.startswith('image/'):
            # It's an image - save it to local file.
            image_ext = guess_extension(res_content_type)
            if not image_ext:
                return
            snapshot_path = ''.join((self.snapshot_path, image_ext))
            image_path = os.path.join(settings.MEDIA_ROOT, snapshot_path)
            image_url = ''.join((settings.MEDIA_URL, snapshot_path))
            with open(image_path, 'wb') as local_image:
                local_image.write(u.read())
            return image_url
        # Some error. Log it.
        if 'application/json' == res_content_type:
            msg = json.load(u)
        else:
            msg = u.read()
        logger.error('%s failed (%s)' % (self, msg))
