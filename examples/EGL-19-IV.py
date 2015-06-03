"""
Example of using cwFitter to generate a HH model for EGL-19 Ca2+ ion channel
Based on experimental data from doi:10.1083/jcb.200203055
"""
import os.path
from neurotune import optimizers
from cwFitter.Initiator import *
from cwFitter.Evaluator import *
from cwFitter.Simulator import *
from cwFitter.Modelator import *

if __name__ == '__main__':

    userData = dict()

    cwd=os.getcwd()
    csv_path = os.path.dirname(cwd)+'/egl-19-IClamp-IV.csv'
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

    myInitiator = Initiator(userData)
    sampleData = myInitiator.getSampleParameters()
    bio_params = myInitiator.getBioParameters()
    # sim_params = myInitiator.getSimParameters(type='IClamp')
    sim_params = myInitiator.getSimParameters()

    myEvaluator = Evaluator(sampleData,sim_params,bio_params)

    candidates = optimizers.CustomOptimizerA(bio_params['max_val_channel'],
                                             bio_params['min_val_channel'],
                                             myEvaluator,
                                             population_size=100,
                                             max_evaluations=600,
                                             num_selected=2,
                                             num_offspring=15,
                                             num_elites=1,
                                             mutation_rate=0.05,
                                             maximize = False,
                                             seeds=None,
                                             verbose=True)

    best_candidate = candidates.optimize(do_plot=True, seed=123)
    best_candidate_params = dict(zip(bio_params['channel_params'],best_candidate))
    cell_var = dict(zip(bio_params['cell_params'],bio_params['val_cell_params']))
    mySimulator = Simulator(sim_params,best_candidate_params,cell_var)
    bestSim = dict()

    # The I/V plot could come from either VClamp or IClamp (VClamp is preferred as is more common)

    if ('VClamp' in sampleData) or (('IV' in sampleData) and (('VClamp' and 'IClamp') not in sampleData)):
        bestSim.update({'VClamp':{}})
        bestSim['VClamp']['t'],bestSim['VClamp']['I'],bestSim['VClamp']['V_max'],bestSim['VClamp']['I_max'] = mySimulator.VClamp()
    if 'IClamp' in sampleData:
        bestSim.update({'IClamp':{}})
        bestSim['IClamp']['t'],bestSim['IClamp']['V'],bestSim['IClamp']['V_max'],bestSim['IClamp']['I_max'] = mySimulator.IClamp()

    myModelator = Modelator(bio_params,sim_params).compare_plots(sampleData,bestSim,show=True)


