"""
Example of using cwFitter to generate a HH model for EGL-19 Ca2+ ion channel
Based on experimental data from doi:10.1083/jcb.200203055
"""

import os.path
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from neurotune import optimizers
from cwFitter import *

def IV_act(V,g,Vhalf,k,a_power,e_rev):
    return g * (1/(1 + np.exp((Vhalf - V)/k)))**int(a_power) * (V - e_rev)

if __name__ == '__main__':

    userData = dict()

    cwd=os.getcwd()
    csv_path = os.path.dirname(cwd)+'/examples/egl-19-IClamp-IV.csv'
    ref = {'fig':'2B','doi':'10.1083/jcb.200203055'}
    x_var = {'type':'Voltage','unit':'V','toSI':1}
    y_var = {'type':'Current','unit':'A/F','toSI':1}
    IV = {'ref':ref,'csv_path':csv_path,'x_var':x_var,'y_var':y_var}
    userData['samples'] = {'IV':IV}

    # csv_path_IC_100 = os.path.dirname(cwd)+'/egl-19-IClamp-100pA.csv'
    # csv_path_IC_200 = os.path.dirname(cwd)+'/egl-19-IClamp-200pA.csv'
    # csv_path_IC_300 = os.path.dirname(cwd)+'/egl-19-IClamp-300pA.csv'
    # csv_path_IC_400 = os.path.dirname(cwd)+'/egl-19-IClamp-400pA.csv'
    # x_var_IC = {'type':'Time','unit':'s','toSI':1}
    # y_var_IC = {'type':'Voltage','unit':'V','toSI':1}
    # traces_IC = [{'amp':100e-12,'csv_path':csv_path_IC_100,'x_var':x_var_IC,'y_var':y_var_IC},
    #              {'amp':200e-12,'csv_path':csv_path_IC_200,'x_var':x_var_IC,'y_var':y_var_IC},
    #              {'amp':300e-12,'csv_path':csv_path_IC_300,'x_var':x_var_IC,'y_var':y_var_IC},
    #              {'amp':400e-12,'csv_path':csv_path_IC_400,'x_var':x_var_IC,'y_var':y_var_IC}]
    # ref_IC = {'fig':'3B','doi':'10.1083/jcb.200203055'}
    # IClamp = {'ref':ref_IC,'traces':traces_IC}
    # userData['samples'] = {'IClamp':IClamp,'IV':IV}

    myInitiator = Initiator.Initiator(userData)
    sampleData = myInitiator.getSampleParameters()
    bio_params = myInitiator.getBioParameters()
    # sim_params = myInitiator.getSimParameters(type='IClamp')
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

    best_candidate = candidates.optimize(do_plot=True, seed=1234)
    # best_candidate = [189.66504757196532, 0.04619592278775828, -0.0015715032129984834, 0.03232782689368996,
    #                   0.0009038799935426481, -0.0006996189007248855, 0.0002076054785033701, 0.5361776032113692,
    #                   2.0, 1.0, 2.9942088447494227e-07, 0.18712673917281542, -1.1396759086697654e-07,
    #                   0.014145060464901655, 1.0]
    best_candidate_params = dict(zip(bio_params['channel_params'],best_candidate))
    cell_var = dict(zip(bio_params['cell_params'],bio_params['val_cell_params']))
    mySimulator = Simulator.Simulator(sim_params,best_candidate_params,cell_var)
    bestSim = dict()

    # The I/V plot could come from either VClamp or IClamp (VClamp is preferred as is more common)

    if ('VClamp' in sampleData) or (('IV' in sampleData) and (('VClamp' and 'IClamp') not in sampleData)):
        bestSim.update({'VClamp':{}})
        bestSim['VClamp']['t'],bestSim['VClamp']['I'],bestSim['VClamp']['V_max'],bestSim['VClamp']['I_max'] = mySimulator.VClamp()
    if 'IClamp' in sampleData:
        bestSim.update({'IClamp':{}})
        bestSim['IClamp']['t'],bestSim['IClamp']['V'],bestSim['IClamp']['V_max'],bestSim['IClamp']['I_max'] = mySimulator.IClamp()

    myModelator = Modelator.Modelator(bio_params,sim_params).compare_plots(sampleData,bestSim,show=True)


    # Fitting to the I/V curve and optimizing parameters
    # According to the literature, the I/V plot coming from steady state currents
    # Only activation expressions will be considered
    vData = np.arange(-0.040, 0.080, 0.001)
    p0 = [best_candidate_params['g'],best_candidate_params['v_half_a'],best_candidate_params['k_a'],best_candidate_params['a_power'],best_candidate_params['e_rev']]

    Vsample = np.asarray(sampleData['IV']['V'])
    Isample = np.asarray(sampleData['IV']['I'])
    popt,pcov = curve_fit(IV_act, Vsample,Isample,p0)
    Iopt = IV_act(vData,popt[0],popt[1],popt[2],popt[3],popt[4])


    print p0
    print popt

    if 'VClamp' in bestSim:
        model_plot, = plt.plot([x*1e3 for x in bestSim['VClamp']['V_max']],bestSim['VClamp']['I_max'], label = 'simulated using GA')
    else:
        model_plot, = plt.plot([x*1e3 for x in bestSim['IClamp']['V_max']],bestSim['IClamp']['I_max'])
    sample, = plt.plot([x*1e3 for x in sampleData['IV']['V']],sampleData['IV']['I'], 'y', label = 'sample data')
    # sim, =plt.plot(vData,I, label = 'simulated_curve')
    opt, =plt.plot([x*1e3 for x in vData],Iopt, 'r', label = 'optimized with GA and curve_fit')
    plt.legend([model_plot,sample,opt])
    # plt.legend([model_plot,sample,opt,sim])
    # plt.legend([sample,opt])
    plt.title("The Best Model fitted to data using GA and SciPy curve_fit")
    plt.ylabel('I (A/F)')
    plt.xlabel('V (mV)')
    plt.show()

