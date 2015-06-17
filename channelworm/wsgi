#!/usr/bin/env python

import os
import sys

## GETTING-STARTED: make sure the next line points to your settings.py:
os.environ['DJANGO_SETTINGS_MODULE'] = 'web_app.settings'

## GETTING-STARTED: make sure the next line points to your django project dir:
sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'web_app'))

virtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],'virtenv')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:execfile(virtualenv, dict(__file__=virtualenv))
except IOError:pass

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
