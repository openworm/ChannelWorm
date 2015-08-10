import rdflib
from adapters import Adapter
from django.db.models import Model


class Exporter(object):
    """
    An Exporter that can be loaded with data, and then export 
    that data as a serialized RDF graph.

    Parameters given when initializing an Exporter are passed to
    `load()`.

    Example usage ::
        
        >>> ex = Exporter(obj1, obj2, obj3)
        >>> ex.load(obj4)
        >>> ex.parse('my_old_graph.n3')
        >>> ex.export('my_new_graph.n3')
    
    In the usage example above, 'my_new_graph.n3' is a serialized
    RDF graph combining the old graph and RDF representations of
    PyOpenWorm objects corresponding to ChannelWorm objects obj1
    through obj4.
    """
    def __init__(self, *args):
        self.data = []
        self.graph = rdflib.Graph()
        self.exported = False
        if args:
            self.load(*args)

    def load(self, *args):
        """
        Load new ChannelWorm data into the Exporter.

        Takes ChannelWorm Django data objects.
        """
        for item in args:
            if not isinstance(item, Model):
                raise TypeError(
                    'Item {} is not instance of {}.'
                    .format(item, type(Model))
                )
            self.data.append(item)

    def parse(self, source=None, format='n3'):
        """
        Load data from a previous graph into the Exporter.

        Parameters
        ----------
        source : string 
            Path to the previous graph.
        format : string (optional)
            Format of the previous graph.
            See `rdflib.graph.Graph.parse.format` for possible values.
        """
        if not source:
            raise TypeError('No data source specified.')
        self.graph.parse(
            source=source,
            format=format
        )

    def export(self, filename=None, format='n3'):
        """
        Export the ChannelWorm data to a flat file that can be
        consumed by PyOpenWorm.

        Parameters
        ----------
        filename : string
            Path to export the serialized graph to.
        format : string (optional)
            Format to serialize in.
            See `rdflib.graph.Graph.parse.format` for possible values.
        """
        if not self.exported:
            for item in self.data:
                item_adapter = Adapter.create(item)
                pyow_object = item_adapter.get_pow()
                trips = pyow_object.triples()
                for triple in trips:
                    self.graph.add(triple)
            self.exported = True

        self.graph.serialize(
            destination=filename,
            format=format
        )

