# configure django to use default settings
# note that this can also be done using an environment variable
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    settings.__file__
except ImproperlyConfigured:
    # load default settings if they're not set
    from channelworm import settings as defaults
    settings.configure(default_settings=defaults, DEBUG=True)

import ion_channel.models as C
import PyOpenWorm as P
from django.forms.models import model_to_dict


class PatchClampAdapter(object):
    """Map a channelworm model to a pyopenworm model"""

    def __init__(self, cw_obj):
        self.channelworm_object = cw_obj
        cw_dict = model_to_dict(self.channelworm_object)

        experiment_id = cw_dict.pop('experiment')
        patch_clamp_id = cw_dict.pop('id')

        self.pyopenworm_object = P.Experiment()

        for key, value in cw_dict:
            self.pyopenworm_object.conditions.set(key, value)

    def get_pow(self):
        return self.pyopenworm_object

    def get_cw(self):
        return self.channelworm_object
