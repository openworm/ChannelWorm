from sciunit import Test
from capabilities import *

class IV_Curve_Test(Test):
    """Compares the IV curve produced by a model to an observed curve"""
    
    def __init__(self, observation=None, name=None):
        Test.__init__(self, observation, name)

    required_capabilities = Generates_IV_Curve

    def generate_prediction(self, model):
        return model.generate_iv_curve()

    score_type = None #need to decide what type of score this will be

    def compute_score(self, observation, prediction):
        pass        #related to above; compute the score

