import PyOpenWorm, pytest, unittest
from ion_channel.adapters import Adapter
from ion_channel.models import (
    IonChannel, Reference, PatchClamp
)


pytestmark = [pytest.mark.django_db]

def test_create_reference(data_pool):
    """Test that we can make a Reference object manually."""
    assert isinstance(data_pool.get_reference(), Reference)

def test_adapt_reference(data_pool):
    """Test that we can map a Reference object to a PyOpenWorm
    Experiment object."""
    r = data_pool.get_reference()

    reference_adapter = Adapter.create(r)

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

def test_create_PatchClamp(data_pool):
    """Test that we can create a PatchClamp object manually."""
    pc = data_pool.get_patch_clamp()
    assert isinstance(pc, PatchClamp)

def test_adapt_PatchClamp(data_pool):
    """
    Test that we can map a PatchClamp object to a PyOpenWorm
    PatchClamp object.
    """
    pc = data_pool.get_patch_clamp()

    pca = Adapter.create(pc)

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

def test_create_ion_channel(data_pool):
    """
    Can we create an IonChannel manually?
    """
    ic = data_pool.get_ion_channel()
    assert isinstance(ic, IonChannel)

@pytest.mark.xfail
def test_adapt_IonChannel(data_pool):
    """
    Test that we can map a IonChannel object to a PyOpenWorm
    Channel object.
    """
    ic = data_pool.get_ion_channel()
    ica = Adapter.create(ic)

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
        'description_evidences': cw_obj.description_evidences,
        'gene_name': cw_obj.gene_name,
        'gene_WB_ID': cw_obj.gene_WB_ID,
        'gene_class': cw_obj.gene_class,
        'proteins': cw_proteins,
        'expression_pattern': cw_obj.expression_pattern,
        'expression_evidences': cw_obj.expression_evidences,
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

    assert pow_dict == cw_dict

def test_adapt_GraphData(data_pool):
    """
    Test that we can map some GraphData to a PyOpenWorm 
    data object.
    """
    graph_data = data_pool.get_graph_data()
    gda = Adapter.create(graph_data)

    cw_obj = gda.get_cw()
    pow_obj = gda.get_pow()

    PyOpenWorm.connect()

    assert cw_obj.asarray() == pow_obj.data

    PyOpenWorm.disconnect()
