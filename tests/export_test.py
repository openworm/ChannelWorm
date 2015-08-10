import os, pytest, rdflib, tempfile
from ion_channel.exporter import Exporter


pytestmark = [pytest.mark.django_db]

SAMPLE_LOCATION = os.path.join('tests', 'test_data', 'rdf_data.n3')
EXPORT_LOCATION = os.path.join('tests', 'test_data', 'exported_data.n3')

def test_exporter_init_and_load(data_pool):
    """
    Can we create an Exporter with arguments?
    Uses IonChannel and Experiment as example data.
    Implicitly tests Exporter's load() method.
    """
    ic = data_pool.get_ion_channel()
    ex = data_pool.get_experiment()
    expo = Exporter(ic, ex)
    assert type(expo) == Exporter

def test_load_type_error():
    """
    Do we get the correct exception if we try to load 
    non-Model data into the Exporter?
    """
    with pytest.raises(TypeError):
        Exporter(None)

def test_parse_without_source():
    """
    When we try to parse without a 'source' argument, do
    we get the correct error type?
    """
    expo = Exporter()
    with pytest.raises(TypeError):
        expo.parse(source=None)

def test_parse():
    """
    Can the parse() method actually parse an RDF graph?
    After parsing, is the graph identical to what RDFLib
    parses?
    """
    expo = Exporter()
    expo.parse(source=SAMPLE_LOCATION)

    graph = rdflib.Graph()
    graph.parse(source=SAMPLE_LOCATION, format='n3')

    assert graph.isomorphic(expo.graph)

def test_load_parse_and_export(data_pool):
    """
    Can we load and parse data, then export it?
    Test passes if we can load, parse and export without
    error, and the resulting graph is the same as one
    previously created with RDFLib.
    """
    fname = tempfile.mktemp()
    expo = Exporter()
    ic = data_pool.get_ion_channel()
    expo.parse(SAMPLE_LOCATION)
    expo.load(ic)
    expo.export(filename=fname)

    current_graph = rdflib.Graph().parse(fname, format='n3')
    known_graph = rdflib.Graph().parse(EXPORT_LOCATION, format='n3')

    assert current_graph.isomorphic(known_graph)

