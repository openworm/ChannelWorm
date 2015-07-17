from django.test import TestCase
import adapters, ion_channel, PyOpenWorm

class AdapterTestCase(TestCase):

    def setUp(self):
        """Run before each test method."""
        self.u = ion_channel.models.User.objects.create(username='user')

    def tearDown(self):
        """Run after each test method."""
        self.u.delete()

    def test_create_Reference(self):
        """Test that we can make a Reference object manually."""
        try:
            test_doi = 'test1212'
            r = ion_channel.models.Reference.objects.create(
                    doi=test_doi,
                    username=self.u
                )
            assert True
        except:
            # throws an exception, so fail
            assert False

    def test_adapt_Reference(self):
        """Test that we can map a Reference object to a PyOpenWorm
        Experiment object."""
        
        r = ion_channel.models.Reference.objects.create(
                username=self.u,
                authors='Einstein et al.',
                doi='123abc',
                PMID='000000',
                title='Hello Worm',
                url='http://example.co.uk',
                year=2001
        )

        reference_adapter = adapters.ReferenceAdapter(r)

        experiment = reference_adapter.get_pow()
        reference = reference_adapter.get_cw()

        PyOpenWorm.connect()

        pyow_dict = {
            'doi': experiment.doi(),
            'pmid': experiment.pmid(),
            'authors': experiment.author(),
            'title': experiment.title(),
            'year': experiment.year(),
            'url': experiment.uri()
        }

        cw_dict = {
            'doi': reference.doi,
            'pmid': reference.PMID,
            'authors': set([reference.authors]),
            'title': reference.title,
            'year': reference.year,
            'url': set([reference.url])
        }

        self.assertEqual(pyow_dict, cw_dict)

