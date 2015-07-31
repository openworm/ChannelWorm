"""
Example of using cwFitter to generate a HH model for ChR2 ion channel expressed in muscle cell
"""

import os.path
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from channelworm.fitter import *

if __name__ == '__main__':

    userData = dict()

    cwd=os.getcwd()

    csv_path_VC = os.path.dirname(cwd)+'/examples/chr2/10.1073pnas.0903570106-1A.csv'
    x_var_VC = {'type':'Time','unit':'ms','toSI':1e-3,'adjust':0}
    y_var_VC = {'type':'Current','unit':'nA','toSI':1e-9,'adjust':0}
    traces_VC = [{'vol':-80e-3,'csv_path':csv_path_VC,'x_var':x_var_VC,'y_var':y_var_VC}]
    ref_VC = {'fig':'1A','doi':'10.1073/pnas.0903570106'}
    VClamp = {'ref':ref_VC,'traces':traces_VC}
    userData['samples'] = {'VClamp':VClamp}

    args = {'weight':{'start':10,'peak':50,'tail':5,'end':5,10:20,11:20,38:5,39:5,41:10}}

    myInitiator = initiators.Initiator(userData)
    sampleData = myInitiator.get_sample_params()
    bio_params = myInitiator.get_bio_params()
    sim_params = myInitiator.get_sim_params()
    myEvaluator = evaluators.Evaluator(sampleData,sim_params,bio_params,args=args)

    # opt = '-pso'
    # opt = '-ga'
    opt = None
    if len(sys.argv) == 2:
        opt = sys.argv[1]

    start = time.time()

    if opt == '-ga':
        ga_args = myInitiator.get_opt_params()
        best_candidate, score = myEvaluator.ga_evaluate(min=bio_params['min_val_channel'],
                                                        max=bio_params['max_val_channel'],
                                                        args=ga_args)
    elif opt == '-pso':
        pso_args = myInitiator.get_opt_params(type='PSO')
        best_candidate, score = myEvaluator.pso_evaluate(lb=bio_params['min_val_channel'],
                                                         ub=bio_params['max_val_channel'],
                                                         args=pso_args)
    else:
        best_candidate = [  9.51961542e-06,  1.49576213e-01,   8.96801324e-02,   4.72151006e-02, 2.86703590e-02,  -5.92876444e-02,  -5.64027680e-03,   5.69842043e-03]

        # PSO (105 min, 100,100), v=None iteration 68: [  4.49957178e-06   6.74566701e-03  -4.01301000e-02   3.76238771e-02 5.22642107e-02  -8.95288556e-02  -1.28559338e-02   6.82972850e-03] 5.86461103488e-16
        # PSO (11 min, 100,100), iteration 68: [  9.51961542e-06   1.49576213e-01   8.96801324e-02   4.72151006e-02 2.86703590e-02  -5.92876444e-02  -5.64027680e-03   5.69842043e-03] 6.8800219817e-16
        # GA after 15 min 3000,6000 : [6.8030549346826835e-06, 0.05725108791016309, 0.04925045000234445, 0.07073784899645463, 0.04786694806633862, -0.08309874276061778, -0.03728574590220146, 0.004800194017168564] : 5.7502562842e-16

    secs = time.time()-start
    print("----------------------------------------------------\n\n"
          +"Ran in %f seconds (%f mins)\n"%(secs, secs/60.0))

    best_candidate_params = dict(zip(bio_params['channel_params'],best_candidate))
    cell_var = dict(zip(bio_params['cell_params'],bio_params['val_cell_params']))
    mySimulator = simulators.Simulator(sim_params,best_candidate_params,cell_var,bio_params['gate_params'])
    bestSim = mySimulator.patch_clamp()

    myModelator = modelators.Modelator(bio_params,sim_params)
    myModelator.compare_plots(sampleData,bestSim,show=True)

    print 'best candidate after optimization:'
    print best_candidate_params

    # Generate NeuroML2 file
    model_params = {}
    model_params['channel_name'] = 'ChR2'
    model_params['channel_id'] = 'ChR2'
    model_params['model_id'] = 'ChR2'
    model_params['contributors'] = [{'name': 'Vahid Ghayoomi','email': 'vahidghayoomi@gmail.com'}]
    model_params['references'] = [{'doi': '10.1073/pnas.0903570106',
                                   'PMID': '19528650',
                                   'citation': 'Liu, Qiang, Gunther Hollopeter, and Erik M. Jorgensen.'
                                               '"Graded synaptic transmission at the Caenorhabditis elegans neuromuscular junction." '
                                               'Proceedings of the National Academy of Sciences 106.26 (2009): 10823-10828.'}]
    model_params['file_name'] = cwd+'/chr2/chr-2.channel.nml'

    nml2_file = myModelator.generate_channel_nml2(bio_params,best_candidate_params,model_params)
