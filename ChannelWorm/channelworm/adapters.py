from channelworm import settings as defaults
from django.conf import settings
settings.configure(default_settings=defaults, DEBUG=True)
import PyOpenWorm as P
import ion_channel.models as C
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

