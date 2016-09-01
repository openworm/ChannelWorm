"""Observations (experimental facts) used to parameterize tests"""

import os, sys
import quantities as pq
import django

path = os.path.realpath(__file__)
for i in range(4):
    path = os.path.split(path)[0]
CW_HOME = path
sys.path.append(CW_HOME)
sys.path.append(os.path.join(CW_HOME,'channelworm')) # Path to 'web_app'

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "web_app.settings"
)
django.setup()
from django.conf import settings
settings.DEBUG = False

# Must be imported after Django setup
from channelworm.ion_channel.models import GraphData

def iv(doi,fig):
    sample_data = GraphData.objects.get(graph__experiment__reference__doi=doi, 
                                        graph__figure_ref_address=fig)
    obs = list(zip(*sample_data.asarray())) 
    iv = {'i/C':obs[1]*pq.A/pq.F, 'v':obs[0]*pq.mV}
    cell_capacitance = 1e-13 * pq.F # Capacitance is arbitrary if IV curves are scaled.  
    iv['i'] = iv['i/C']*cell_capacitance
    return iv

egl19_iv = iv('10.1083/jcb.200203055','2B')
slo2_iv = iv('10.1113/jphysiol.2010.200683','7B')