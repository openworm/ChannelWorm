from django.test import TestCase
import adapters, PyOpenWorm, unittest, random
from ion_channel.models import *

# TODO: Run object creation only once.
#       This could be accomplished by having a create_SomeObject 
#       function that creates an object, and returns the already-made 
#       object if called a second time.
#           Or: We could find a good way to "mock" objects and their
#               attributes...

class AdapterTestCase(TestCase):

    def setUp(self):
        """Run before each test method."""
        self.u = User.objects.create(username='user')

    def tearDown(self):
        """Run after each test method."""
        self.u.delete()

    def test_create_Reference(self):
        """Test that we can make a Reference object manually."""
        test_doi = 'test1212'
        r = Reference.objects.create(
                doi=test_doi,
                username=self.u
        )
        assert isinstance(r, Reference)

    def test_adapt_Reference(self):
        """Test that we can map a Reference object to a PyOpenWorm
        Experiment object."""
        
        r = Reference.objects.create(
            PMID='000000',
            authors='Einstein et al.',
            doi='123abc',
            title='Hello Worm',
            url='http://example.co.uk',
            username=self.u,
            year=2001
        )

        reference_adapter = adapters.ReferenceAdapter(r)

        experiment = reference_adapter.get_pow()
        reference = reference_adapter.get_cw()

        PyOpenWorm.connect()

        pyow_dict = {
            'authors': experiment.author,
            'doi': experiment.doi,
            'pmid': experiment.pmid,
            'title': experiment.title,
            'url': experiment.uri,
            'year': experiment.year
        }

        cw_dict = {
            'authors': reference.authors,
            'doi': reference.doi,
            'pmid': reference.PMID,
            'title': reference.title,
            'url': reference.url,
            'year': reference.year
        }

        self.assertEqual(pyow_dict, cw_dict)

    def test_create_PatchClamp(self):
        """Test that we can create a PatchClamp object manually."""
        ref = Reference.objects.create(
            username=self.u,
            doi='somedoi',
        )

        ex = Experiment.objects.create(
            reference=ref,
            username=self.u,
        )

        ic = IonChannel.objects.create(
            channel_name='fake'
        )

        pc = PatchClamp.objects.create(
            deltat=100, 
            duration=200, 
            end_time=200, 
            experiment=ex,
            ion_channel=ic,
            protocol_end=200, 
            protocol_start=0, 
            protocol_step=100, 
            start_time=0, 
        )
        assert isinstance(pc, PatchClamp)

    def test_adapt_PatchClamp(self):
        """Test that we can map a PatchClamp object to a PyOpenWorm
        PatchClamp object."""
        ref = Reference.objects.create(
            username=self.u,
            doi='somedoi',
        )

        ex = Experiment.objects.create(
            reference=ref,
            username=self.u,
        )

        ic = IonChannel.objects.create(
            channel_name='fake'
        )

        params = {
            'deltat': 100, 
            'duration': 200, 
            'end_time': 200, 
            'experiment': ex,
            'ion_channel': ic,
            'protocol_end': 200, 
            'protocol_start': 0, 
            'protocol_step': 100, 
            'start_time': 0, 
        }


        pc = PatchClamp.objects.create(**params)
        
        pca = adapters.PatchClampAdapter(pc)

        cw_obj = pca.get_cw()
        pow_obj = pca.get_pow()

        #import pdb; pdb.set_trace()

        cw_dict = {
            'deltat': cw_obj.deltat,
            'duration': cw_obj.duration,
            'end_time': cw_obj.end_time,
            'experiment': cw_obj.experiment,
            'ion_channel': cw_obj.ion_channel,
            'protocol_end': cw_obj.protocol_end,
            'protocol_start': cw_obj.protocol_start,
            'protocol_step': cw_obj.protocol_step,
            'start_time': cw_obj.start_time,
        }

        pow_dict = {
            'deltat': cw_obj.deltat,
            'duration': cw_obj.duration,
            'end_time': cw_obj.end_time,
            'experiment': cw_obj.experiment,
            'ion_channel': cw_obj.ion_channel,
            'protocol_end': cw_obj.protocol_end,
            'protocol_start': cw_obj.protocol_start,
            'protocol_step': cw_obj.protocol_step,
            'start_time': cw_obj.start_time,
        }

        assert cw_dict == pow_dict
