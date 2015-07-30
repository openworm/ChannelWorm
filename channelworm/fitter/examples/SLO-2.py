"""
Example of using cwFitter to generate a HH model for SLO-2 ion channel
Based on experimental data from doi:10.1083/jcb.200203055
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

    csv_path_VC_1 = os.path.dirname(cwd)+'/examples/slo-2-VClamp/1.csv'
    csv_path_VC_2 = os.path.dirname(cwd)+'/examples/slo-2-VClamp/2.csv'
    csv_path_VC_3 = os.path.dirname(cwd)+'/examples/slo-2-VClamp/3.csv'
    csv_path_VC_4 = os.path.dirname(cwd)+'/examples/slo-2-VClamp/4.csv'
    x_var_VC = {'type':'Time','unit':'ms','toSI':1e-3}
    y_var_VC = {'type':'Current','unit':'nA','toSI':1e-9,'adjust':-0.82}
    traces_VC = [{'vol':110e-3,'csv_path':csv_path_VC_1,'x_var':x_var_VC,'y_var':y_var_VC},
                 {'vol':None,'csv_path':csv_path_VC_2,'x_var':x_var_VC,'y_var':y_var_VC},
                 {'vol':-110e-3,'csv_path':csv_path_VC_3,'x_var':x_var_VC,'y_var':y_var_VC},]
                 # {'vol':-90e-3,'csv_path':csv_path_VC_4,'x_var':x_var_VC,'y_var':y_var_VC}]
    ref_VC = {'fig':'6a','doi':'10.1038/77670'}
    VClamp = {'ref':ref_VC,'traces':traces_VC}
    # #
    # csv_path_VC = os.path.dirname(cwd)+'/examples/slo-2/SLO-2-2000-VClamp.csv'
    # x_var_VC = {'type':'Time','unit':'ms','toSI':1e-3}
    # y_var_VC = {'type':'Current','unit':'nA','toSI':1e-9,'adjust':-0.82}
    # traces_VC = [{'csv_path':csv_path_VC,'x_var':x_var_VC,'y_var':y_var_VC}]
    # ref_VC = {'fig':'6a','doi':'10.1038/77670'}
    # VClamp = {'ref':ref_VC,'traces':traces_VC}
    #
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

    # userData['samples'] = {'IV':IV,'POV':POV}
    # userData['samples'] = {'VClamp':VClamp}
    userData['samples'] = {'IV':IV,'POV':POV,'VClamp':VClamp}

    myInitiator = initiators.Initiator(userData)
    sampleData = myInitiator.get_sample_params()
    bio_params = myInitiator.get_bio_params()
    sim_params = myInitiator.get_sim_params()
    myEvaluator = evaluators.Evaluator(sampleData,sim_params,bio_params)

    # opt = '-pso'
    # opt = '-ga'
    opt = None
    if len(sys.argv) == 2:
        opt = sys.argv[1]

    if ('IV' or 'POV') in sampleData and opt is not None:
        while True:
            q = raw_input("\n\nTry fitting curves (y,n):")
            if q == "n":
                break  # stops the loop
            elif q == "y":

                # Find initial guess for parameters using curve_fit, leastsq

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
                    if 'POV' in sampleData:
                        POV_fit_cost = myEvaluator.pov_cost(popt)
                        print 'POV cost:'
                        print POV_fit_cost
                    vData = np.arange(-0.140, 0.110, 0.001)
                    Iopt = mySimulator.iv_act(vData,*popt)
                    plt.plot([x*1e3 for x in bestSim['V_max']],bestSim['I_max'], label = 'Initial parameters', color='y')
                    plt.plot([x*1e3 for x in sampleData['IV']['V']],sampleData['IV']['I'], color='k', label = 'sample data')
                    plt.plot([x*1e3 for x in vData],Iopt, color='r', label = 'Fitted to IV curve')
                    plt.legend()
                    plt.title("IV Curve Fit")
                    plt.xlabel('V (mV)')
                    plt.ylabel('I (A)')
                    plt.show()

                elif 'POV' in sampleData:

                    popt , p0 = mySimulator.optim_curve(params= bio_params['channel_params'],
                                                        best_candidate= best_candidate,
                                                        target= [sampleData['POV']['V'],sampleData['POV']['PO']],curve_type='POV')

                    print 'Params after POV minimization:'
                    print p0
                    POV_fit_cost = myEvaluator.pov_cost(popt)
                    print 'POV cost:'
                    print POV_fit_cost

                    vData = np.arange(-0.140, 0.110, 0.001)
                    POopt = mySimulator.pov_act(vData,*popt)
                    plt.plot([x*1e3 for x in bestSim['V_PO_max']],bestSim['PO_max'], label = 'Initial parameters', color='y')
                    plt.plot([x*1e3 for x in sampleData['POV']['V']],sampleData['POV']['PO'], color='k', label = 'sample data')
                    plt.plot([x*1e3 for x in vData],POopt, color='r', label = 'Fitted to G/Gmax vs V curve')
                    plt.legend()
                    plt.title("G/Gmax vs V Curve Fit")
                    plt.xlabel('V (mV)')
                    plt.ylabel('G/Gmax')
                    plt.show()

                if popt is not None:
                    if opt == '-pso':
                        bio_params['min_val_channel'][0:4] = popt[0:4] - abs(popt[0:4]/2)
                        bio_params['max_val_channel'][0:4] = popt[0:4] + abs(popt[0:4]/2)
                    else:
                        bio_params['min_val_channel'][0:4] = popt[0:4]
                        bio_params['max_val_channel'][0:4] = popt[0:4]

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
        # best_candidate = [2.678373586024887e-08, -0.004343196320916513, -0.15148699378068883, 0.04457177073153084, 0.0006512657782666903]
        best_candidate = [2.6713432536911465e-08, -0.0043477407996737093, -0.077423632426596764, 0.030752484500400822, 0.0007076266889846564]

    secs = time.time()-start
    print("----------------------------------------------------\n\n"
          +"Ran in %f seconds (%f mins)\n"%(secs, secs/60.0))

    best_candidate_params = dict(zip(bio_params['channel_params'],best_candidate))
    cell_var = dict(zip(bio_params['cell_params'],bio_params['val_cell_params']))
    mySimulator = simulators.Simulator(sim_params,best_candidate_params,cell_var,bio_params['gate_params'])
    bestSim = mySimulator.patch_clamp()

    myModelator = modelators.Modelator(bio_params,sim_params).compare_plots(sampleData,bestSim,show=True)

    print 'best candidate after optimization:'
    print best_candidate_params
