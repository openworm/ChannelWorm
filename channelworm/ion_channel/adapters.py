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

    Specific Adapters should override this class.

    Subclasses must define a mapping between attributes called "pyow_to_cw",
    as well as the two classes to be mapped between: "pyopenworm_class" and 
    "channelworm_class".

    The Adapter superclass takes care of mapping between the values, but 
    anything else that needs to be done should be written in the __init__
    method for the subclass. See the IonChannelAdapter subclass for an
    example of this.

    Attributes
    ----------

    channelworm_object : A representation of the object in ChannelWorm form
    pyopenworm_object : A representation of the object in PyOpenWorm form

    Parameters
    ----------

    cw_obj : The input ChannelWorm object

    Example usage ::

        >>> from adapters import Adapter
        >>> from ion_channel.models import PatchClamp 
        # get some saved patch-clamp experiment from CW
        >>> cw_patch = PatchClamp.objects.all()[0]
        # create an adapter object with it
        >>> pca = Adapter.create(cw_patch)
        # get back the corresponding PyOW model
        >>> pca.get_pow()
        Experiment(reference=`Evidence(AssertsAllAbout(), year=`None', title=`SALAM', doi=`Salam')', Conditions())
        # assign the PyOW to a variable and use it elsewhere
        >>> pyow_patch = pca.get_pow()
 
    """

    @classmethod
    def create(cls, input_object):
        """
        Create an object using the correct Adapter subclass,
        based on the type of the input object.
        """
        input_type = type(input_object)
        for subclass in cls.__subclasses__():
            if subclass.channelworm_class == input_type:
                return subclass(input_object)

    def map_properties(self):
        """
        Map between the properties defined in the subclass.
        """

        # initialize PyOpenWorm connection so we can access its API
        P.connect()

        # initialize pyopenworm object
        self.pyopenworm_object = self.pyopenworm_class()

        for p, c in self.pyow_to_cw.items():
            cw_value = getattr(self.channelworm_object, c)
            pow_property = getattr(self.pyopenworm_object, p)
            map(pow_property, [cw_value])

        P.disconnect()

    def get_pow(self):
        """Return the PyOpenWorm representation of the object"""
        return self.pyopenworm_object

    def get_cw(self):
        """Return the ChannelWorm representation of the object"""
        return self.channelworm_object


class ReferenceAdapter(Adapter):
    """
    Map a ChannelWorm Reference object to a PyOpenWorm Evidence.
    """
    pyopenworm_class = P.Evidence
    channelworm_class = C.Reference

    pyow_to_cw = {
        'author': 'authors',
        'doi': 'doi',
        'pmid': 'PMID',
        'title': 'title',
        'uri': 'url',
        'year': 'year',
    }

    def __init__(self, cw_obj):
        self.channelworm_object = cw_obj
        self.map_properties()


class PatchClampAdapter(Adapter):
    """
    Map a channelworm patch clamp model to a pyopenworm model.

    """
    pyopenworm_class = P.PatchClampExperiment
    channelworm_class = C.PatchClamp

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

    def __init__(self, cw_obj):
        self.channelworm_object = cw_obj
        self.map_properties()

class IonChannelAdapter(Adapter):
    """
    Map a ChannelWorm IonChannel to a PyOpenWorm Channel.
    """
    pyopenworm_class = P.Channel
    channelworm_class = C.IonChannel

    pyow_to_cw = {
        'name': 'channel_name',
        'description': 'description',
        'gene_name': 'gene_name',
        'gene_WB_ID': 'gene_WB_ID',
   #     'gene_class': 'gene_class',
        'expression_pattern': 'expression_pattern',
    }

    def __init__(self, cw_obj):
        self.channelworm_object = cw_obj
        self.map_properties()

        P.connect()
        # mapping evidence to Assertions
        pmids = cw_obj.expression_evidences.split(', ')
        for pmid in pmids:
            e = P.Evidence()
            e.pmid(pmid)
            e.asserts(self.pyopenworm_object.expression_pattern)
            e.save()

        pmids = cw_obj.description_evidences.split(', ')
        for pmid in pmids:
            e = P.Evidence()
            e.pmid(pmid)
            e.asserts(self.pyopenworm_object.description)
            e.save()

        # proteins in CW are ;-delimited, but should be 
        #multiple values in PyOpenWorm
        pros = cw_obj.proteins.split('; ')
        for p in pros:
            self.pyopenworm_object.proteins(p)

