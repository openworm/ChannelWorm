import adapters

class Exporter(object):
    """
    An Exporter can be loaded with data, and then export 
    that data to a flat file.
    """
    def __init__(self, *args):
        self.data = []
        if args:
            self.load(*args)

    def load(self, *args):
        """
        Load data into the Exporter.
        """
        for item in args:
            print(item)
            self.data.append(item)

    def export(self, filename):
        """
        Export the ChannelWorm data to a flat file that can be
        consumed by PyOpenWorm.
        """
        for item in self.data:
            # call adapter on each item
            # do something with resulting PyOW objects
            pass # (for now)
