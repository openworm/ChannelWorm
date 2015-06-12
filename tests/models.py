import sciunit
import capabilities

class IonChannelModel(sciunit.Model, capabilities.Generates_IV_Curve,
        capabilities.Receives_Current, capabilities.Generates_Membrane_Potential):
        """A generic ion channel model."""

        def __init__(self, name=None, iv_curve=None, current=None, voltage=None):
            super(IonChannelModel, self).__init__(name=name)

        def generate_iv_curve(self):
            return self.iv_curve

        def receive_current(self):
            #Not clear what this should return
            pass

        def generate_membrane_potential(self):
            #Not clear what this should return
            pass
