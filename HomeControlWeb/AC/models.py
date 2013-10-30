import logging

from django.db import models

from common import load_json_from_url

class AcControl(models.Model):
    POWER_ON = 'ON'
    POWER_OFF = 'OFF'
    POWER_UNKNOWN = 'TBD'
    POWER_STATES = (
        (POWER_ON, 'On'),
        (POWER_OFF, 'Off'),
        (POWER_UNKNOWN, 'Unknown'),
    )
    
    MODE_COOL = 0
    MODE_HEAT = 1
    MODE_FAN = 2
    MODE_MODES = (
        (MODE_COOL, 'Cool'),
        (MODE_HEAT, 'Heat'),
        (MODE_FAN, 'Fan'),
    )
    
    FAN_AUTO = 0
    FAN_LOW = 1
    FAN_MEDIUM = 2
    FAN_HIGH = 3
    FAN_SPEEDS = (
        (FAN_AUTO, 'Auto'),
        (FAN_LOW, 'Low'),
        (FAN_MEDIUM, 'Medium'),
        (FAN_HIGH, 'High'),
    )
    
    # A/C name
    name = models.CharField(max_length=100, unique=True)
    # Cached power state from last successful command
    power_state = models.CharField(max_length=3, choices=POWER_STATES,
                                   default=POWER_UNKNOWN)
    # Cached mode from last successful command
    mode = models.PositiveSmallIntegerField(choices=MODE_MODES,
                                            default=MODE_COOL)
    # Cached fan speed from last successful command
    fan = models.PositiveSmallIntegerField(choices=FAN_SPEEDS,
                                            default=FAN_AUTO)
    # Cached temperature from last successful command
    temp = models.PositiveSmallIntegerField(default=25)
    # A/C-RPC URL
    rpc_url = models.URLField(default='http://localhost:8000/AC/')
    
    def __unicode__(self):
        return self.name
    
    def command(self, params):
        "Send A/C command via RPC app and update state based on response"
        res = load_json_from_url(self.rpc_url, 'command',
                            pwr=params.get('power'), mode=params.get('mode'),
                            fan=params.get('fan'), temp=params.get('temp'))
        # Update cached state for successful command
        if 'Success' == res:
            if '1' == params.get('power'):
                self.power_state = self.POWER_ON
            else:
                if self.POWER_ON == self.power_state:
                    self.power_state = self.POWER_OFF
                elif self.POWER_OFF == self.power_state:
                    self.power_state = self.POWER_ON
                else:
                    self.power_state = self.POWER_UNKNOWN
            self.mode = int(params.get('mode'))
            self.fan = int(params.get('fan'))
            self.temp = int(params.get('temp'))
            self.save()
        return res
