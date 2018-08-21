from sciunit import TestSuite

import tests as t

def hook(test, tests, score, **kwargs):
    score.plot()

egl19_suite = TestSuite('EGL-19 IV Curves',t.egl19_iv_test,
                        include_models = ['EGL-19*'],
                        hooks={t.egl19_iv_test:{'f':hook}})
slo2_suite = TestSuite('SLO-2 IV Curves',t.slo2_iv_test,
                       include_models = ['SLO-2*'],
                       hooks={t.slo2_iv_test:{'f':hook}})

suites = [egl19_suite,slo2_suite]
