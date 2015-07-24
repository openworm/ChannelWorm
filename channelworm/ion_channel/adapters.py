# configure django to use default settings
# note that this can also be done using an environment variable
import sys
sys.path.append('..')
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

class Adapter(object):
    """
    An interface used to map between PyOpenWorm and ChannelWorm data
    objects.

    Attributes
    ----------

    channelworm_object : A representation of the object in ChannelWorm form
    pyopenworm_object : A representation of the object in PyOpenWorm form

    Parameters
    ----------

    cw_obj : The input ChannelWorm object
    """

    def get_pow(self):
        """Return the PyOpenWorm representation of the object"""
        return self.pyopenworm_object

    def get_cw(self):
        """Return the ChannelWorm representation of the object"""
        return self.channelworm_object


class ReferenceAdapter(Adapter):
    """
    Map a channelworm Reference object to a PyOpenWorm Evidence.
    """

    def __init__(self, cw_obj):
        # initialize PyOpenWorm connection so we can access its API
        P.connect()

        self.channelworm_object = cw_obj
        self.pyopenworm_object = P.Evidence()

        pyow_to_cw = {
            'author': 'authors',
            'doi': 'doi',
            'pmid': 'PMID',
            'title': 'title',
            'uri': 'url',
            'year': 'year',
        }

        for p, c in pyow_to_cw.items():
            cw_attr = getattr(self.channelworm_object, c)
            setattr(self.pyopenworm_object, p, cw_attr)

        P.disconnect()


class PatchClampAdapter(Adapter):
    """
    Map a channelworm patch clamp model to a pyopenworm model.

    Example usage ::

        >>> import adapters
        >>> cw_patch = C.PatchClamp.objects.all()[0]    # get some saved patch-clamp experiment from CW
        >>> pca = adapters.PatchClampAdapter(cw_patch)    # create an adapter object with it
        >>> pca.get_pow()    # get back the corresponding PyOW model
        Experiment(reference=`Evidence(AssertsAllAbout(), year=`None', title=`SALAM', doi=`Salam')', Conditions())
        >>> pyow_patch = pca.get_pow()    # assign the PyOW to a variable and use it elsewhere
    
        """

    def __init__(self, cw_obj):
        # initialize PyOpenWorm connection so we can access its API
        P.connect()

        self.pyopenworm_object = P.PatchClampExperiment()
        self.channelworm_object = cw_obj

        #this is just a 1:1 mapping of attributes, but let's spell it
        # out for consistency
        pyow_to_cw = {
            'Ca_concentration': 'Ca_concentration',
            'Cl_concentration': 'Cl_concentration',
            'blockers': 'blockers',
            'cell': 'cell',
            'cell_age': 'cell_age',
            'delta_t': 'deltat',
            'duration': 'duration',
            'end_time': 'end_time',
            'extra_solution': 'extra_solution',
            'initial_voltage': 'initial_voltage',
            'ion_channel': 'ion_channel',
            'membrane_capacitance': 'membrane_capacitance',
            'mutants': 'mutants',
            'patch_type': 'patch_type',
            'pipette_solution': 'pipette_solution',
            'protocol_end': 'protocol_end',
            'protocol_start': 'protocol_start',
            'protocol_step': 'protocol_step',
            'start_time': 'start_time',
            'temperature': 'temperature',
            'type': 'type',
        }
 
        for p, c in pyow_to_cw.items():
            cw_attr = getattr(self.channelworm_object, c)
            setattr(self.pyopenworm_object, p, cw_attr)

        # we no longer need PyOW API so we can kill the connection
        P.disconnect()

