# configure django to use default settings
# note that this can also be done using an environment variable
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if hasattr(settings, 'DEBUG'):
    # settings are configured already
    pass
else:
    # load default settings if they're not set
    from web_app import settings as defaults
    settings.configure(default_settings=defaults, DEBUG=True)

import ion_channel.models as C
import PyOpenWorm as P
from django.forms.models import model_to_dict


class PatchClampAdapter(object):
    """Map a channelworm model to a pyopenworm model"""

    def __init__(self, cw_obj):
        # initialize PyOpenWorm connection so we can access its API
        P.connect()

        self.channelworm_object = cw_obj
        cw_dict = model_to_dict(self.channelworm_object)

        experiment_id = cw_dict.pop('experiment')
        patch_clamp_id = cw_dict.pop('id')

        self.pyopenworm_object = P.Experiment()
        
        # get the CW model's experiment
        cw_evidence = C.Experiment.objects.get(id=experiment_id)

        # make a PyOW evidence object with it
        pow_evidence = P.Evidence(doi=cw_evidence.doi)

        # add it to the PyOW experiment model
        self.pyopenworm_object.reference(pow_evidence)

        for key, value in cw_dict.iteritems():
            self.pyopenworm_object.conditions.set(key, value)

        # we not longer need PyOW API so we can kill the connection
        P.disconnect()

    def get_pow(self):
        return self.pyopenworm_object

    def get_cw(self):
        return self.channelworm_object
