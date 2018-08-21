"""
ChannelWorm fitter module for validating generated models.
"""

from neuroml.utils import validate_neuroml2

class Validator(object):
    """
    Validate new model and compare with existing ones
    """

    def __init__(self):
        """

        :return:
        """

    def bestModel(self, channel_type):
        """
        Takes an Ion channel and returns the best model generated.
        """

    def validate_nml2(self, nml2_file):
        """
        Validated NeuroML2 file
        """

        return validate_neuroml2(nml2_file)
