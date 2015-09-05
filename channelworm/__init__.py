__author__ = 'vahid'

import sys
import os
import django

CHANNELWORM_PATH = os.path.dirname(os.path.realpath(__file__))

def django_setup():
    if CHANNELWORM_PATH not in sys.path:
        sys.path.append(CHANNELWORM_PATH)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "web_app.settings") # web_app should be an app on the channelworm path.  
#    django.setup()
    
    
