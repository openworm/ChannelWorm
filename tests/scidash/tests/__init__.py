from neuronunit.tests.channel import IVCurvePeakTest
from . import observations as obs

egl19_iv_test = IVCurvePeakTest(obs.egl19_iv, name='EGL-19 IV', scale=True)
slo2_iv_test = IVCurvePeakTest(obs.slo2_iv, name='SLO-2 IV', scale=False)
# SLO-2 test doesn't using scaling because model prediction is so bad that
# the sign is wrong, so the scale factor that maximizes agreement with the 
# data is 0!  

tests = []#egl19_iv_test]