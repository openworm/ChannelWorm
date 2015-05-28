# This file holds our models (at least for now)

import sciunit
import random

from sciunit import Score,ErrorScore,InvalidScoreError

# create a Score type
class BooleanScore(Score):
    """
    A boolean score. Must be True or False.
    """

    def __init__(self, score, related_data={}):
        if isinstance(score,Exception) or score in [True,False]:
            super(BooleanScore,self).__init__(score, related_data=related_data)
        else:
            raise InvalidScoreError("Score must be True or False.")

    @property
    def sort_key(self):
        if self.score == True:
            return 1.0
        elif self.score == False:
            return 0.0
        else:
            return 'N/A'

    def __str__(self):
        if self.score == True:
            return 'Pass'
        elif self.score == False:
            return 'Fail'
        else:
            return 'N/A'

# create a Capability
class ReturnsNumber(sciunit.Capability):
    """ This Model returns a real number. """

    def return_num(self):
        raise NotImplementedError("Must return a real number.")

# create a Model that has the above Capability
class RandomSample(sciunit.Model, ReturnsNumber):
    """ Generates a random number between 1 and 10. """

    def __init__(self):
        self.return_num()

    def return_num(self):
        return random.randint(3, 3)

# create a class of Test
class SingleNumberTest(sciunit.Test):
    """Tests that a single a single predicted number is equal to an observed one."""
    def __init__(self, observation=None, name=None):
        sciunit.Test.__init__(self, observation, name)

    required_capabilities = ReturnsNumber,

    def generate_prediction(self, model):
        return model.return_num()

    score_type = BooleanScore

    def compute_score(self, observation, prediction):
        return self.score_type(prediction == observation)

def this_is_a_test():
    # create an instance of a test
    pass_test = SingleNumberTest(3)

    # create a model
    random_model = RandomSample()

    # convert the test result to a string (either "Pass" or "Fail")
    # and compare it to "Pass"
    # this test should pass one in three times
    # NOTE: it might be better to have the `assert` statement inside another method,
    # since comparing strings is rough (and would only work with booleans)
    assert(str(pass_test.judge(random_model)) == "Pass")
