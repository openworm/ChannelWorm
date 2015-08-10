import pytest
import ion_channel.models as models
from django.test import TestCase
from ion_channel.adapters import Adapter
from ion_channel.exporter import Exporter


class ExporterTestCase(TestCase):

    def test_init_exporter(self):
        """
        Can we create an Exporter with arguments?
        Uses IonChannel and Experiment as example data.
        """
        ic = atc.get_ion_channel()
        ex = atc.get_experiment()
        expo = Exporter(ic, ex)
        assert type(expo) == Exporter

    def test_load_type_error(self):
        """
        Do we get the correct exception if we try to load 
        non-Model data into the Exporter?
        """
        with pytest.raises(TypeError):
            Exporter(None)


