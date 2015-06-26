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

from channelworm.ion_channel import models as C
import PyOpenWorm as P
from django.forms.models import model_to_dict


class PatchClampAdapter(object):
    """
    Map a channelworm patch clamp model to a pyopenworm model.

    Example usage ::

        >>> import adapters
        >>> cw_patch = ion_channel.models.PatchClamp.objects.all()[0]    # get some saved patch-clamp experiment from CW
        >>> pca = adapters.PatchClampAdapter(cw_patch)    # create an adapter object with it
        >>> pca.get_pow()    # get back the corresponding PyOW model
        Experiment(reference=`Evidence(AssertsAllAbout(), year=`None', title=`SALAM', doi=`Salam')', Conditions())
        >>> pyow_patch = pca.get_pow()    # assign the PyOW to a variable and use it elsewhere
    
    Attributes
    ----------

    channelworm_object : A representation of the object in ChannelWorm form
    pyopenworm_object : A representation of the object in PyOpenWorm form

    Parameters
    ----------

    cw_obj : The input ChannelWorm object
    """

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

        # we no longer need PyOW API so we can kill the connection
        P.disconnect()

    def get_pow(self):
        """Return the PyOpenWorm representation of the object"""
        return self.pyopenworm_object

    def get_cw(self):
        """Return the ChannelWorm representation of the object"""
        return self.channelworm_object
