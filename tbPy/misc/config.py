from collections import namedtuple
import json

class Config(object):

    def __init__(self, settings):
        self.settings = settings
    
    def grab_setting(self, key):
        for k, v in self.settings.items():
            if key == k:
                return v
        return None