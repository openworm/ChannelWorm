import pytest
from django.utils import timezone
from channelworm.ion_channel.models import (
    IonChannel, Reference, Experiment, 
    PatchClamp, User, Graph, GraphData
)


@pytest.fixture(scope='session')
def data_pool():
    return DataPool()

class DataPool(object):
    """
    Session-level pytest fixture (see 'data_pool()' above)
    which can create a data object of several types, or return
    one if it has been created previously.

    Implementation of the 'Object Pool' design pattern.
    """
    def get_user(self):
        """
        Fixture for getting a User object.
        If we already created one, we can just get it
        rather than making another.
        """
        if not hasattr(self, 'user'):
            self.user = User.objects.create(username='user')

        return self.user

    def get_reference(self):
        """
        Fixture for getting a Reference object.
        """
        if not hasattr(self, 'reference'):
            self.reference = Reference.objects.create(
                PMID='000000',
                authors='Einstein et al.',
                create_date=timezone.now(),
                doi='123abc',
                title='Hello Worm',
                url='http://example.co.uk',
                username=self.get_user(),
                year=2001,
            )

        return self.reference

    def get_experiment(self):
        """
        Fixture for getting an Experiment object.
        """
        if not hasattr(self, 'experiment'):
            self.experiment = Experiment.objects.create(
                reference=self.get_reference(),
                username=self.get_user(),
                create_date=timezone.now(),
            )

        return self.experiment

    def get_ion_channel(self):
        """
        Fixture for getting an IonChannel object.
        """
        if not hasattr(self, 'ion_channel'):
            self.ion_channel = IonChannel.objects.create(
                channel_name='CNN',
                description='Yup, it is a channel.',
                description_evidences='0000000, 000001',
                gene_name='Gene Clark',
                gene_WB_ID='Wbbt:123456',
                gene_class='Working Class',
                proteins='BRD-5, isoform a; BRD-5, isoform b',
                expression_pattern='Have you seen the Silver Raven?',
                expression_evidences='000000, 000002',
            )

        return self.ion_channel

    def get_patch_clamp(self):
        """
        Fixture for getting a PatchClamp object.
        """
        if not hasattr(self, 'patch_clamp'):
            self.patch_clamp = PatchClamp.objects.create(
                deltat=100,
                duration=200,
                end_time=200,
                experiment=self.get_experiment(),
                ion_channel=self.get_ion_channel(),
                protocol_end=200,
                protocol_start=0,
                protocol_step=100,
                start_time=0,
            )

        return self.patch_clamp

    def get_graph(self):
        """
        Fixture for getting a Graph object
        """
        if not hasattr(self, 'graph'):
            self.graph = Graph.objects.create()

        return self.graph

    def get_graph_data(self):
        """
        Fixture for getting a GraphData object.
        The data here should be representative of what
        we can expect from the digitization process.
        """
        if not hasattr(self, 'graph_data'):
            self.graph_data = GraphData.objects.create(
                graph=self.get_graph(),
                series_data=(
                    "90, 0.773809523809524\r\n"
                    "80, 0.6714285714285715\r\n"
                    "70.25, 0.567857142857143\r\n"
                    "60.25, 0.4464285714285715\r\n"
                    "50.25, 0.33571428571428574\r\n"
                    "40.25, 0.23571428571428577\r\n"
                    "30.25, 0.15833333333333333\r\n"
                    "20.25, 0.10595238095238102\r\n"
                    "10.25, 0.06785714285714284\r\n"
                    "0.25, 0.04285714285714293\r\n"
                    "-9.75, 0.026190476190476097\r\n"
                    "-20, 0.014285714285714235\r\n"
                    "-30, 0.0071428571428571175\r\n"
                    "-39.75, 0.0023809523809523725\r\n"
                    "-49.75, 0.0011904761904761862\r\n"
                    "-59.5, -0.0035714285714285587\r\n"
                    "-69.5, -0.0035714285714285587\r\n"
                    "-79.75, -0.0023809523809523725\r\n"
                    "-89.75, -0.0023809523809523725\r\n"
                )
            )

        return self.graph_data
