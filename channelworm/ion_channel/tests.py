from django.test import TestCase
from django.utils import timezone
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
        
        now = timezone.now()

        r = Reference.objects.create(
            PMID='000000',
            authors='Einstein et al.',
            create_date=now,
            doi='123abc',
            title='Hello Worm',
            url='http://example.co.uk',
            username=self.u,
            year=2001,
        )

        reference_adapter = adapters.ReferenceAdapter(r)

        experiment = reference_adapter.get_pow()
        reference = reference_adapter.get_cw()

        PyOpenWorm.connect()

        pyow_dict = {
            'authors': experiment.author(),
            'doi': experiment.doi(),
            'pmid': experiment.pmid(),
            'title': experiment.title(),
            'url': experiment.uri(),
            'year': experiment.year(),
        }

        cw_dict = {
            'authors': set([reference.authors]),
            'doi': reference.doi,
            'pmid': reference.PMID,
            'title': reference.title,
            'url': set([reference.url]),
            'year': reference.year
        }

        PyOpenWorm.disconnect()

        assert pyow_dict == cw_dict

    def test_create_PatchClamp(self):
        """Test that we can create a PatchClamp object manually."""
 
        now = timezone.now()

        ref = Reference.objects.create(
            username=self.u,
            doi='somedoi',
        )

        ex = Experiment.objects.create(
            reference=ref,
            username=self.u,
            create_date=now
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
        """
        Test that we can map a PatchClamp object to a PyOpenWorm
        PatchClamp object.
        """

        now = timezone.now()

        ref = Reference.objects.create(
            username=self.u,
            doi='somedoi',
        )

        ex = Experiment.objects.create(
            reference=ref,
            username=self.u,
            create_date=now,
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

        PyOpenWorm.connect()

        pow_dict = {
            'delta_t': pow_obj.delta_t(),
            'duration': pow_obj.duration(),
            'end_time': pow_obj.end_time(),
            'ion_channel': pow_obj.ion_channel(),
            'protocol_end': pow_obj.protocol_end(),
            'protocol_start': pow_obj.protocol_start(),
            'protocol_step': pow_obj.protocol_step(),
            'start_time': pow_obj.start_time(),
        }

        cw_dict = {
            'delta_t': cw_obj.deltat,
            'duration': cw_obj.duration,
            'end_time': cw_obj.end_time,
            'ion_channel': cw_obj.ion_channel,
            'protocol_end': cw_obj.protocol_end,
            'protocol_start': cw_obj.protocol_start,
            'protocol_step': cw_obj.protocol_step,
            'start_time': cw_obj.start_time,
        }

        PyOpenWorm.disconnect()

        assert cw_dict == pow_dict

    def test_create_ion_channel(self):
        """
        Can we create an IonChannel manually?
        """
        ic = IonChannel.objects.create(
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

        assert isinstance(ic, IonChannel)

    @unittest.expectedFailure
    def test_adapt_IonChannel(self):
        """
        Test that we can map a IonChannel object to a PyOpenWorm
        Channel object.
        """

        ic = IonChannel.objects.create(
            channel_name='CNN',
            description=u'Yup, it is a channel.',
            description_evidences='000003, 000001',
            gene_name='Gene Clark',
            gene_WB_ID='Wbbt:123456',
            gene_class='Working Class',
            proteins='BRD-5, isoform a; BRD-5, isoform b',
            expression_pattern=u'Have you seen the Silver Raven?',
            expression_evidences='000005, 000002',
        )

        ica = adapters.IonChannelAdapter(ic)

        cw_obj = ica.get_cw()
        pow_obj = ica.get_pow()

        # parse PMIDs for expression_patterns, 
        # then for descriptions
        # and finally proteins
        exp_strings = cw_obj.expression_evidences.split(', ')
        cw_expression_pmids = set(int(s) for s in exp_strings)

        desc_strings = cw_obj.description_evidences.split(', ')
        cw_description_pmids = set(int(s) for s in desc_strings)

        cw_proteins = set(cw_obj.proteins.split('; '))

        cw_dict = {
            'channel_name': cw_obj.channel_name,
            'description': cw_obj.description,
            'description_evidences': cw_obj.description_evidences,#coerce to set
            'gene_name': cw_obj.gene_name,
            'gene_WB_ID': cw_obj.gene_WB_ID,
            'gene_class': cw_obj.gene_class,
            'proteins': cw_proteins,
            'expression_pattern': cw_obj.expression_pattern,
            'expression_evidences': cw_obj.expression_evidences,#coerce to set
        }

        # retrieve PMIDs for expression_patterns, 
        # then for descriptions
        ev = PyOpenWorm.Evidence()
        ev.asserts(pow_obj.expression_pattern)
        pow_expression_pmids = set(e.pmid() for e in ev.load())

        ev = PyOpenWorm.Evidence()
        ev.asserts(pow_obj.description)
        pow_description_pmids = set(e.pmid() for e in ev.load())

        pow_dict = {
            'channel_name': pow_obj.name(),
            'description': pow_obj.description(),
            'description_evidences': pow_description_pmids,
            'gene_name': pow_obj.gene_name(),
            'gene_WB_ID': pow_obj.gene_WB_ID(),
            'gene_class': pow_obj.gene_class(),
            'proteins': pow_obj.proteins(),
            'expression_pattern': pow_obj.expression_pattern(),
            'expression_evidences': pow_expression_pmids,
        }

        self.maxDiff = None
        self.assertEqual( pow_dict , cw_dict)
