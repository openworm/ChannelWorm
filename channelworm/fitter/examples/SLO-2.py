"""
Example of using cwFitter to generate a HH model for EGL-19 Ca2+ ion channel
Based on experimental data from doi:10.1083/jcb.200203055
"""

import os.path
import time
import numpy as np
import matplotlib.pyplot as plt
from neurotune import optimizers
from channelworm.fitter import *
from metapub import pubmedfetcher

if __name__ == '__main__':

    userData = dict()

    cwd=os.getcwd()

    csv_path = os.path.dirname(cwd)+'/examples/slo-2/SLO-2-2000-IV.csv'
    ref = {'fig':'6a','doi':'10.1038/77670'}
    x_var = {'type':'Voltage','unit':'mV','toSI':1e-3}
    y_var = {'type':'Current','unit':'pA','toSI':1e-12}
    IV = {'ref':ref,'csv_path':csv_path,'x_var':x_var,'y_var':y_var}

    csv_path_POV = os.path.dirname(cwd)+'/examples/slo-2/SLO-2-2000-GV.csv'
    ref_POV = {'fig':'6b','doi':'10.1038/77670'}
    x_var_POV = {'type':'Voltage','unit':'mV','toSI':1e-3}
    y_var_POV = {'type':'G/Gmax','unit':'','toSI':1}
    POV = {'ref':ref_POV,'csv_path':csv_path_POV,'x_var':x_var_POV,'y_var':y_var_POV}
    userData['samples'] = {'IV':IV,'POV':POV}

    myInitiator = Initiator.Initiator(userData)
    sampleData = myInitiator.getSampleParameters()
    bio_params = myInitiator.getBioParameters()
    sim_params = myInitiator.getSimParameters()
    myEvaluator = Evaluator.Evaluator(sampleData,sim_params,bio_params)

    candidates = optimizers.CustomOptimizerA(bio_params['max_val_channel'],
                                             bio_params['min_val_channel'],
                                             myEvaluator,
                                             population_size=300, #20 times larger than free parameters
                                             max_evaluations=600,
                                             num_selected=2,
                                             num_offspring=15,
                                             num_elites=1,
                                             mutation_rate=0.05,
                                             maximize = False,
                                             seeds=None,
                                             verbose=True)

    start = time.time()

    best_candidate, score = candidates.optimize(do_plot=True, seed=1234)

    secs = time.time()-start
    print("----------------------------------------------------\n\n"
          +"Ran in %f seconds (%f mins)\n"%(secs, secs/60.0))

    # best_candidate = [414.09006856420586, -0.003533360676786078, -0.15, 0.060088036241820124, 0.013330322127824196, 4.0]

    best_candidate_params = dict(zip(bio_params['channel_params'],best_candidate))
    cell_var = dict(zip(bio_params['cell_params'],bio_params['val_cell_params']))
    mySimulator = Simulator.Simulator(sim_params,best_candidate_params,cell_var)
    bestSim = mySimulator.patch_clamp()

    myModelator = Modelator.Modelator(bio_params,sim_params).compare_plots(sampleData,bestSim,show=True)

    if 'IV' in sampleData:

        popt , p0 = mySimulator.optim_curve(params= bio_params['channel_params'],
                                            best_candidate= best_candidate,
                                            target= [sampleData['IV']['V'],sampleData['IV']['I']])

        print best_candidate_params
        print p0
        print popt

        vData = np.arange(-0.140, 0.110, 0.001)
        Iopt = mySimulator.IV_act(vData,*popt)
        model_plot, = plt.plot([x*1e3 for x in bestSim['V_max']],bestSim['I_max'], label = 'simulated using GA', color='y')

        sample, = plt.plot([x*1e3 for x in sampleData['IV']['V']],sampleData['IV']['I'], color='k', label = 'sample data')
        opt, =plt.plot([x*1e3 for x in vData],Iopt, color='r', label = 'optimized with GA and curve_fit')
        plt.legend([model_plot,sample,opt])
        plt.title("The Best Model fitted to data using GA and SciPy curve_fit")
        plt.ylabel('I (A)')
        plt.xlabel('V (mV)')
        plt.show()
