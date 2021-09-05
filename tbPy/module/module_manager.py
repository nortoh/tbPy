import importlib
import os

class ModuleManager(object):

    def __init__(self):
        self.modules_loaded = dict()

        if not os.path.exists('modules'):
            os.makedirs('modules')

    
    def load_modules(self):
        module_files = os.listdir('modules')

    def load_module(self, module):
        pass