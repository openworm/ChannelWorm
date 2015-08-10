import rdflib
from adapters import Adapter
from django.db.models import Model

class Exporter(object):
    """
    An Exporter can be loaded with data, and then export 
    that data to a flat file.
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
        Load data from the previous graph into the Exporter.
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
        """
        if not self.exported:
            for item in self.data:
                item_adapter = Adapter.create(item)
                pyow_object = item_adapter.get_pow()
                trips = pyow_object.triples()
                for triple in trips:
                    self.graph.add(trip)
            self.exported = True

        self.graph.serialize(
            destination=filename,
            format=format
        )

