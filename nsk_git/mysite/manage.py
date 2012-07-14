#!/usr/bin/env python
import sys #code for remote debugging with autoreload on
from django.core.management import execute_manager
import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    #import sys #original code
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings

#code for remote debugging with autoreload on

command = None
if len(sys.argv) != 1:
    command = sys.argv[1]
    
if settings.DEBUG and (command == 'runserver' or command == 'testserver'):
    try:
        import pydevd
        inEclipse = True
    except ImportError:
        inEclipse = False

    if inEclipse:
        from django.utils import autoreload
        m = autoreload.main
        def main(main_func, args=None, kwargs=None):
            import os
            if os.environ.get("RUN_MAIN") == 'true':
                def pydevdDecorator(func):
                    def wrap(*args, **kws):
                        pydevd.settrace(suspend = False)
                        return func()
                    return wrap
                main_func = pydevdDecorator(main_func)
            
            return m(main_func)
    
        autoreload.main = main

#end code for remote debugging with autoreload on

if __name__ == "__main__":
    execute_manager(settings)
