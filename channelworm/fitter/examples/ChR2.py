"""
Example of using cwFitter to generate a HH model for ChR2 ion channel expressed in muscle cell
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

    csv_path_VC = os.path.dirname(cwd)+'/examples/chr2-data/chr2-vc.csv'
    x_var_VC = {'type':'Time','unit':'ms','toSI':1e-3,'adjust':0}
    y_var_VC = {'type':'Current','unit':'pA','toSI':1e-12,'adjust':0}
    traces_VC = [{'vol':-80e-3,'csv_path':csv_path_VC,'x_var':x_var_VC,'y_var':y_var_VC}]
    ref_VC = {'fig':'1A','doi':'10.1073/pnas.0903570106'}
    VClamp = {'ref':ref_VC,'traces':traces_VC}
    userData['samples'] = {'VClamp':VClamp}

    args = {'weight':{'start':10,'peak':30,'tail':15,'end':10,21:25,25:15,27:30,28:5,29:15}}

    myInitiator = initiators.Initiator(userData)
    sampleData = myInitiator.get_sample_params()
    bio_params = myInitiator.get_bio_params()
    sim_params = myInitiator.get_sim_params()
    # myEvaluator = evaluators.Evaluator(sampleData,sim_params,bio_params,args=args)
    myEvaluator = evaluators.Evaluator(sampleData,sim_params,bio_params)

    # bio parameters for CHR-2
    bio_params['cell_type'] = 'ADAL'
    bio_params['channel_type'] = 'ChR-2'
    bio_params['ion_type'] = 'Ca'
    bio_params['gate_params'] = {'vda': {'power': 1},'vdi': {'power': 1}}

    bio_params['channel_params'] = ['g_dens','e_rev']
    bio_params['unit_chan_params'] = ['S/m2','V']
    bio_params['min_val_channel'] = [1, -1e-3]
    bio_params['max_val_channel'] = [10, 1e-3]

    bio_params['channel_params'].extend(['v_half_a','k_a','T_a'])
    bio_params['unit_chan_params'].extend(['V','V','s'])
    bio_params['min_val_channel'].extend([-1e-3, 0.0001, 5e-3])
    bio_params['max_val_channel'].extend([ 1e-3,   0.1,  15e-3])

    bio_params['channel_params'].extend(['v_half_i','k_i','T_i'])
    bio_params['unit_chan_params'].extend(['V','V','s'])
    bio_params['min_val_channel'].extend([-1e-3, -0.1,  20e-3])
    bio_params['max_val_channel'].extend([ 1e-3, -1e-6, 60e-3])

    # Simulation parameters for chr2 VClamp
    sim_params['v_hold'] = 0
    sim_params['I_init'] = 0
    sim_params['pc_type'] = 'VClamp'
    sim_params['deltat'] = 1e-4
    sim_params['duration'] = 1.430
    sim_params['start_time'] = 0.2
    sim_params['end_time'] = 1.230
    sim_params['protocol_start'] = -80e-3
    sim_params['protocol_end'] = 80e-3
    sim_params['protocol_steps'] = 10e-3
    sim_params['ca_con'] = 6e-6

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
        pso_args['minstep'] = 1e-26
        pso_args['minfunc'] = 1e-28
        pso_args['swarmsize'] = 500
        pso_args['maxiter'] = 100
        best_candidate, score = myEvaluator.pso_evaluate(lb=bio_params['min_val_channel'],
                                                         ub=bio_params['max_val_channel'],
                                                         args=pso_args)
    else:
        best_candidate = [ 3.51608078,  0.541046,   -0.01707861,  0.03200137,  0.03444286, -0.09601821, -0.00484456,  0.01502828]

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

    # Now fitting to curve using curve_fit(leastsq)
    if 'Clamp' in sampleData:
        for trace in sampleData['VClamp']['traces']:
            if 'vol' in trace:
                if trace['vol'] is None:
                    pass
                else:
                    end = sim_params['protocol_end']
                    start = sim_params['protocol_start']
                    sim_params['protocol_end'] = trace['vol']
                    sim_params['protocol_start'] = trace['vol']

                    x = np.asarray(trace['t'])
                    on = sim_params['start_time']
                    off = sim_params['end_time']
                    dur = sim_params['duration']
                    onset = np.abs(x-on).argmin()
                    offset = np.abs(x-off).argmin()
                    # t_sample_on = trace['t'][onset+1:offset]
                    t_sample_on = trace['t'][onset:]
                    # t_sample_on = trace['t']
                    # I_sample_on = trace['I'][onset+1:offset]
                    I_sample_on = trace['I'][onset:]
                    # I_sample_on = trace['I']

                    vcSim = simulators.Simulator(sim_params,best_candidate_params,cell_var,bio_params['gate_params'])
                    pcSim = vcSim.patch_clamp()
                    popt , p0 = vcSim.optim_curve(params= bio_params['channel_params'],
                                                  best_candidate= best_candidate,
                                                  target= [t_sample_on,I_sample_on],curve_type='VClamp')
                    vcEval =  evaluators.Evaluator(sampleData,sim_params,bio_params)

                    print 'Params after VClamp minimization:'
                    print p0
                    print popt

                    VClamp_fit_cost = vcEval.vclamp_cost(popt)
                    print 'VClamp cost:'
                    print VClamp_fit_cost
                    # tData = np.arange(on, off, sim_params['deltat'])
                    tData = np.arange(on, dur, sim_params['deltat'])
                    # tData = np.arange(0, dur, sim_params['deltat'])
                    Iopt = vcSim.patch_clamp(tData,*popt)
                    plt.plot(pcSim['t'],pcSim['I'][0], label = 'Initial parameters', color='y')
                    plt.plot(t_sample_on,I_sample_on, '--ko', label = 'sample data')
                    plt.plot(tData,Iopt, color='r', label = 'Fitted to VClamp trace')
                    plt.legend(loc=9, bbox_to_anchor=(0.9, 0.1))
                    plt.title('VClamp Curve Fit for holding potential %i (mV)'%(trace['vol']*1e3))
                    plt.xlabel('T (s)')
                    plt.ylabel('I (A)')
                    plt.show()

                    sim_params['protocol_end'] = end
                    sim_params['protocol_start'] = start

                    # best_candidate_params = dict(zip(bio_params['channel_params'],popt))
                    # cell_var = dict(zip(bio_params['cell_params'],bio_params['val_cell_params']))
                    # mySimulator = simulators.Simulator(sim_params,best_candidate_params,cell_var,bio_params['gate_params'])
                    # bestSim = mySimulator.patch_clamp()
                    #
                    # myModelator = modelators.Modelator(bio_params,sim_params)
                    # myModelator.compare_plots(sampleData,bestSim,show=True)

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
    model_params['file_name'] = cwd+'/chr2-data/chr-2.channel.nml'

    nml2_file = myModelator.generate_channel_nml2(bio_params,best_candidate_params,model_params)
    run_nml_out = myModelator.run_nml2(model_params['file_name'])