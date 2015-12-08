"""
Test models to make sure modules working well
"""

import os.path
import sys

sys.path.append('../../..')
from channelworm.fitter import *

if __name__ == '__main__':

    cwd=os.getcwd()
    path = cwd+'/test-data/'
    if not os.path.exists(path):
        os.makedirs(path)

    sampleData = {}
    myInitiator = initiators.Initiator()
    bio_params = myInitiator.get_bio_params()
    sim_params = myInitiator.get_sim_params()

    bio_params['cell_type'] = 'Xenopus oocytes'
    bio_params['channel_type'] = 'Na_HH'
    bio_params['ion_type'] = 'Na'
    bio_params['val_cell_params'][0] = 200e-9 # C_mem DOI: 10.1074/jbc.M605814200
    bio_params['val_cell_params'][1] = 20e-6 # area DOI: 10.1101/pdb.top066308
    # bio_params['gate_params'] = {'m': {'power': 1}}
    bio_params['gate_params'] = {'m': {'power': 3},'h': {'power': 1}}

    sim_params['v_hold'] = -90e-3
    sim_params['I_init'] = 0
    sim_params['pc_type'] = 'VClamp'
    sim_params['deltat'] = 1e-4
    sim_params['duration'] = 1.2
    sim_params['start_time'] = 0.05
    sim_params['end_time'] = 1.050
    sim_params['protocol_start'] = -90e-3
    sim_params['protocol_end'] = 90e-3
    sim_params['protocol_steps'] = 10e-3

    best_candidate_params = {'g_dens':12,'e_rev':50e-3}
    best_candidate_params.update({'v_half_m_a':-29e-3, 'v_half_m_b':0,'k_m_a':0.0055,'k_m_b':15e-3, 'rate_m_a':2.77,
                       'rate_m_b':0.3,'a_m_a':0,'a_m_b':1,'b_m_a':1,'b_m_b':0,'c_m_a':-1,'c_m_b':1,'d_m_a':1,'d_m_b':-1,'m_power':3})
    best_candidate_params.update({'v_half_h_a':0, 'v_half_h_b':-20e-3,'k_h_a':20e-3,'k_h_b':10e-3, 'rate_h_a':0.014,
                       'rate_h_b':2.8,'a_h_a':1,'a_h_b':1,'b_h_a':0,'b_h_b':1,'c_h_a':1,'c_h_b':1,'d_h_a':-1,'d_h_b':1,'h_power':1})

    bcp = best_candidate_params

    bcp['a_m_a'] = int(bcp['a_m_a'])
    bcp['b_m_a'] = int(bcp['b_m_a'])
    bcp['c_m_a'] = int(bcp['c_m_a'])
    bcp['d_m_a'] = int(bcp['d_m_a'])
    bcp['a_m_b'] = int(bcp['a_m_b'])
    bcp['b_m_b'] = int(bcp['b_m_b'])
    bcp['c_m_b'] = int(bcp['c_m_b'])
    bcp['d_m_b'] = int(bcp['d_m_b'])

    best_candidate_params = bcp

    print 'expression: rate*(a OR (V-mu)/k))/ (b + c*exp(-d*(V-mu)/k)))'
    print 'Alpha:'
    print '(%.2f*(%i OR (V-%.2f)/%.2f))/(%.2f + %i*exp(-%i*(V-%.2f)/%.2f)))' \
          %(bcp['rate_m_a'],int(bcp['a_m_a']),bcp['v_half_m_a']*1e3,bcp['k_m_a']*1e3,int(bcp['b_m_a']),int(bcp['c_m_a']),
            int(bcp['d_m_a']),bcp['v_half_m_a']*1e3,bcp['k_m_a']*1e3)
    print 'Beta:'
    print '(%.2f*(%i OR (V-%.2f)/%.2f))/(%.2f + %i*exp(-%i*(V-%.2f)/%.2f)))' \
          %(bcp['rate_m_b'],int(bcp['a_m_b']),bcp['v_half_m_b']*1e3,bcp['k_m_b']*1e3,int(bcp['b_m_b']),int(bcp['c_m_b']),
            int(bcp['d_m_b']),bcp['v_half_m_b']*1e3,bcp['k_m_b']*1e3)

    cell_var = dict(zip(bio_params['cell_params'],bio_params['val_cell_params']))
    mySimulator = simulators.Simulator(sim_params,best_candidate_params,cell_var,bio_params['gate_params'])
    bestSim = mySimulator.patch_clamp()
    myModelator = modelators.Modelator(bio_params,sim_params)
    myModelator.patch_clamp_plots(bestSim, show=True, path=path)

    # To generate better plots
    sim_params['protocol_steps'] = 1e-3
    mySimulator = simulators.Simulator(sim_params,best_candidate_params,cell_var,bio_params['gate_params'])
    bestSim = mySimulator.patch_clamp()
    myModelator = modelators.Modelator(bio_params,sim_params)
    myModelator.gating_plots(bestSim, show=True, path=path)
