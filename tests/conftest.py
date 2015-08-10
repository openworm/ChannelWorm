import pytest
from django.utils import timezone
from ion_channel.models import (
    IonChannel, Reference, Experiment, PatchClamp, User
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

