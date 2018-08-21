"""
Example of using cwFitter to generate a HH model for EGL-19 Ca2+ ion channel
Based on experimental data from doi:10.1083/jcb.200203055
"""

import os.path
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('../../..')
from channelworm.fitter import *

if __name__ == '__main__':

    userData = dict()

    cwd=os.getcwd()
    csv_path = os.path.dirname(cwd)+'/examples/egl-19-data/egl-19-IClamp-IV.csv'
    ref = {'fig':'2B','doi':'10.1083/jcb.200203055'}
    x_var = {'type':'Voltage','unit':'V','toSI':1}
    y_var = {'type':'Current','unit':'A/F','toSI':75e-12}
    IV = {'ref':ref,'csv_path':csv_path,'x_var':x_var,'y_var':y_var}
    userData['samples'] = {'IV':IV}

    # csv_path_IC_100 = os.path.dirname(cwd)+'egl-19-data//egl-19-IClamp-100pA.csv'
    # csv_path_IC_200 = os.path.dirname(cwd)+'egl-19-data//egl-19-IClamp-200pA.csv'
    # csv_path_IC_300 = os.path.dirname(cwd)+'egl-19-data//egl-19-IClamp-300pA.csv'
    # csv_path_IC_400 = os.path.dirname(cwd)+'egl-19-data//egl-19-IClamp-400pA.csv'
    # x_var_IC = {'type':'Time','unit':'s','toSI':1}
    # y_var_IC = {'type':'Voltage','unit':'V','toSI':1}
    # traces_IC = [{'amp':100e-12,'csv_path':csv_path_IC_100,'x_var':x_var_IC,'y_var':y_var_IC},
    #              {'amp':200e-12,'csv_path':csv_path_IC_200,'x_var':x_var_IC,'y_var':y_var_IC},
    #              {'amp':300e-12,'csv_path':csv_path_IC_300,'x_var':x_var_IC,'y_var':y_var_IC},
    #              {'amp':400e-12,'csv_path':csv_path_IC_400,'x_var':x_var_IC,'y_var':y_var_IC}]
    # ref_IC = {'fig':'3B','doi':'10.1083/jcb.200203055'}
    # IClamp = {'ref':ref_IC,'traces':traces_IC}
    # userData['samples'] = {'IClamp':IClamp,'IV':IV}

    myInitiator = initiators.Initiator(userData)
    sampleData = myInitiator.get_sample_params()
    bio_params = myInitiator.get_bio_params()
    sim_params = myInitiator.get_sim_params()
    myEvaluator = evaluators.Evaluator(sampleData,sim_params,bio_params)

    # bio parameters for SLO-2
    bio_params['cell_type'] = 'ADAL'
    bio_params['channel_type'] = 'EGL-19'
    bio_params['ion_type'] = 'Ca'
    bio_params['val_cell_params'][0] = 75e-12 # C_mem DOI: 10.1074/jbc.M605814200
    bio_params['val_cell_params'][1] = 75e-10 # area DOI: 10.1101/pdb.top066308
    bio_params['gate_params'] = {'vda': {'power': 2}}

    bio_params['channel_params'] = ['g_dens','e_rev']
    bio_params['unit_chan_params'] = ['S/m2','V']
    bio_params['min_val_channel'] = [1,  40e-3]
    bio_params['max_val_channel'] = [10, 70e-3]

    bio_params['channel_params'].extend(['v_half_a','k_a','T_a'])
    bio_params['unit_chan_params'].extend(['V','V','s'])
    bio_params['min_val_channel'].extend([-10e-3, 4e-3, 0.0001])
    bio_params['max_val_channel'].extend([ 30e-3, 20e-3, 2e-3])

    # Simulation parameters for EGL-19 I/V
    sim_params['v_hold'] = -70e-3
    sim_params['I_init'] = 0
    sim_params['pc_type'] = 'VClamp'
    sim_params['deltat'] = 1e-5
    sim_params['duration'] = 0.03
    sim_params['start_time'] = 0.002
    sim_params['end_time'] = 0.022
    sim_params['protocol_start'] = -40e-3
    sim_params['protocol_end'] = 80e-3
    sim_params['protocol_steps'] = 10e-3

    opt = '-pso'
    # opt = '-ga'
    # opt = None
    if len(sys.argv) == 2:
        opt = sys.argv[1]

    if 'IV' in sampleData and opt is not None:
        while True:
            q = raw_input("\n\nTry fitting curves (y,n):")
            if q == "n":
                break  # stops the loop
            elif q == "y":

                # Find initial guess for parameters using curve_fit, leastsq

                popt = None
                best_candidate = np.asarray(bio_params['min_val_channel']) + np.asarray(bio_params['max_val_channel']) / 2

                best_candidate_params = dict(zip(bio_params['channel_params'],best_candidate))
                cell_var = dict(zip(bio_params['cell_params'],bio_params['val_cell_params']))
                mySimulator = simulators.Simulator(sim_params,best_candidate_params,cell_var,bio_params['gate_params'])
                bestSim = mySimulator.patch_clamp()

                if 'IV' in sampleData:

                    popt , p0 = mySimulator.optim_curve(params= bio_params['channel_params'],
                                                        best_candidate= best_candidate,
                                                        target= [sampleData['IV']['V'],sampleData['IV']['I']])

                    print 'Params after IV minimization:'
                    print p0
                    IV_fit_cost = myEvaluator.iv_cost(popt)
                    print 'IV cost:'
                    print IV_fit_cost
                    if 'VClamp' in sampleData:
                        VClamp_fit_cost = myEvaluator.vclamp_cost(popt)
                        print 'VClamp cost:'
                        print VClamp_fit_cost
                    vData = np.arange(-0.040, 0.080, 0.001)
                    Iopt = mySimulator.iv_act(vData,*popt)
                    plt.plot([x*1 for x in bestSim['V_ss']],bestSim['I_ss'], label = 'Initial parameters', color='y')
                    plt.plot([x*1 for x in sampleData['IV']['V']],sampleData['IV']['I'], '--ko', label = 'sample data')
                    plt.plot([x*1 for x in vData],Iopt, color='r', label = 'Fitted to IV curve')
                    plt.legend()
                    plt.title("IV Curve Fit")
                    plt.xlabel('V (mV)')
                    plt.ylabel('I (A)')
                    plt.show()

                if popt is not None:
                    if opt == '-pso':
                        bio_params['min_val_channel'][0:4] = popt[0:4] - abs(popt[0:4]/2)
                        bio_params['max_val_channel'][0:4] = popt[0:4] + abs(popt[0:4]/2)
                    else:
                        bio_params['min_val_channel'][0:4] = popt[0:4]
                        bio_params['max_val_channel'][0:4] = popt[0:4]

                    best_candidate_params = dict(zip(bio_params['channel_params'],popt))
                    cell_var = dict(zip(bio_params['cell_params'],bio_params['val_cell_params']))
                    mySimulator = simulators.Simulator(sim_params,best_candidate_params,cell_var,bio_params['gate_params'])
                    bestSim = mySimulator.patch_clamp()

                    myModelator = modelators.Modelator(bio_params,sim_params)
                    myModelator.compare_plots(sampleData,bestSim,show=True)
                    myModelator.ss_plots(bestSim,show=True)
