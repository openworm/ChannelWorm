# this file will hold the Capabilities that our Models can have

import sciunit

class Receives_Current(sciunit.Capability):
    """ This model can receive a current when simulated. """

    def receive_current(self):
        raise NotImplementedError("receives_current not implemented")

class Generates_Membrane_Potential(sciunit.Capability):
    """ This model can produce a membrane potential when simulated. """

    def generate_membrane_potential(self):
        raise NotImplementedError("generates_membrane_potential not implemented")

class Generates_IV_Curve(Receives_Current, Generates_Membrane_Potential, sciunit.Capability):
    """ This model can generate an IV curve when simulated. """

    def generate_iv_curve(self):
        raise NotImplementedError("generate_iv_curve not implemented")

