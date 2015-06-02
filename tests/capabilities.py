# this file will hold the Capabilities that our Models can have

import sciunit

class Generates_IV_Curve(sciunit.Capability, Receives_Current, Generates_Membrane_Potential):
    """ This model can generate and IV curve when simulated. """

    def generate_iv_curve(self):
        raise NotImplementedError("generate_iv_curve not implemented")

class Receives_Current(sciunit.Capability):
    """ This model can receive a current when simluated. """

    def receive_current(self):
        raise NotImplementedError("receives_current not implemented")

class Generates_Membrane_Potential(sciunit.Capability):
    """ This model can produce a membrane potential when simluated. """

    def generate_membrane_potential(self):
        raise NotImplementedError("generates_membrane_potential not implemented")
