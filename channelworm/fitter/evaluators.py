"""
ChannelWorm fitter module for evaluating parameters optimized by searching algorithms.
"""

import numpy as np
from channelworm.fitter.simulators import Simulator
from heapq import nsmallest
import copy
from neurotune import optimizers
from pyswarm import pso

class Evaluator(object):

    def __init__(self, sampleData, sim_params, bio_params, scale=False, args={}):

        self.sampleData = sampleData
        self.sim_params = sim_params
        self.bio_params = bio_params
        self.scale = scale
        self.pso_flag = False
        self.mySimulator = None

        # Define minimum acceptable cost value for constraints
        if 'func' in args:
            self.func = args['func']
        else:
            self.func = self.vclamp_cost

        if 'IV_dist' in args:
            self.IV_dist = args['IV_dist']
        else:
            self.IV_dist = 1e-20

        if 'POV_dist' in args:
            self.POV_dist = args['POV_dist']
        else:
            self.POV_dist = 8e-3

        if 'I_dist' in args:
            self.I_dist = args['I_dist']
        else:
            self.I_dist = 1e-8

        if 'V_dist' in args:
            self.V_dist = args['V_dist']
        else:
            self.V_dist = 1e-20

        if 'weight' in args:
            self.weight = args['weight']
        else:
            self.weight = {'start':10,'peak':50,'tail':30,'end':10}

    def ga_evaluate(self,min,max,args={}):
        """
        Optimization using Genetics algorithm (GA).

        :param min: Minimum values for parameters
        :param max: Maximum values for parameters
        :param args: Optional arguments for neurotune optimizer
        :return: optimized values
        """

        # Initialize neurotune optional arguments
        if 'population_size' in args:
            population_size = args['population_size']
        else:
            population_size = 100
        if 'max_evaluations' in args:
            max_evaluations = args['max_evaluations']
        else:
            max_evaluations = 100
        if 'num_selected' in args:
            num_selected = args['num_selected']
        else:
            num_selected = None
        if 'num_offspring' in args:
            num_offspring = args['num_offspring']
        else:
            num_offspring = None
        if 'num_elites' in args:
            num_elites = args['num_elites']
        else:
            num_elites = 1
        if 'mutation_rate' in args:
            mutation_rate = args['mutation_rate']
        else:
            mutation_rate = 0.2
        if 'maximize' in args:
            maximize = args['maximize']
        else:
            maximize = False
        if 'seeds' in args:
            seeds = args['seeds']
        else:
            seeds = []
        if 'verbose' in args:
            verbose = args['verbose']
        else:
            verbose = False

        candidates = optimizers.CustomOptimizerA(max_constraints=max,
                                                 min_constraints=min,
                                                 evaluator=self,
                                                 population_size=population_size, #20 times larger than free parameters
                                                 max_evaluations=max_evaluations,
                                                 num_selected=num_selected,
                                                 num_offspring=num_offspring,
                                                 num_elites=num_elites,
                                                 mutation_rate=mutation_rate,
                                                 maximize = maximize,
                                                 seeds=seeds,
                                                 verbose=verbose)

        best_candidate, score = candidates.optimize(do_plot=True, seed=1234)

        return best_candidate,score

    def evaluate(self, candidates, args=[]):
        """
        Runs VClamp and/or IClamp simulation to calculate the cost value for each candidate.
        I/V curve is also considered as an evaluation factor and coming from VClamp or IClamp simulations.
        The approach is based on Gurkiewicz & Korngreen study (doi:10.1371/journal.pcbi.0030169.)

        :param: candidates: Candidate set from the GA that should be evaluated.
        :param: args: arguments if needed (based on Inspyred requirements for evaluate function)
        :return: total_fitness
        """

        fitness = 1e10
        total_fitness = []
        Vcost = 0
        Icost = 0
        IVcost = 0
        POVcost = 0
        cell_var = dict(zip(self.bio_params['cell_params'],self.bio_params['val_cell_params']))

        for candidate in candidates:
            samples = 0
            cand_var = dict(zip(self.bio_params['channel_params'],candidate))
            self.mySimulator = Simulator(self.sim_params,cand_var,cell_var,self.bio_params['gate_params']).patch_clamp()

            if 'POV' in self.sampleData:
                POVcost = self.pov_cost(candidate)
                samples +=1
                if self.pso_flag == False or self.func == self.pov_cost:
                    fitness = POVcost
                elif POVcost > self.POV_dist:
                    fitness = 1e10
                    total_fitness.append(fitness)
                    continue

            if 'IV' in self.sampleData:
                IVcost = self.iv_cost(candidate)
                samples +=1
                if self.pso_flag == False or self.func == self.iv_cost:
                    fitness = IVcost
                elif IVcost > self.IV_dist:
                    fitness = 1e10
                    total_fitness.append(fitness)
                    continue

            if 'VClamp' in self.sampleData:
                Vcost = self.vclamp_cost(candidate)
                samples +=1
                if self.pso_flag == False or self.func == self.vclamp_cost:
                    fitness = Vcost
                elif Vcost > self.V_dist:
                    fitness = 1e10
                    total_fitness.append(fitness)
                    continue

            if 'IClamp' in self.sampleData:
                Icost = self.iclamp_cost(candidate)
                samples +=1
                if self.pso_flag == False or self.func == self.iclamp_cost:
                    fitness = Icost
                elif Icost > self.I_dist:
                    fitness = 1e10
                    total_fitness.append(fitness)
                    continue

            if self.pso_flag == False:
                fitness = (Vcost + Icost + IVcost + POVcost) / samples

            total_fitness.append(fitness)

        return total_fitness

    def vclamp_cost(self,candidate):

        if (self.pso_flag and self.func == self.vclamp_cost) or self.mySimulator is None:
            cand_var = dict(zip(self.bio_params['channel_params'],candidate))
            cell_var = dict(zip(self.bio_params['cell_params'],self.bio_params['val_cell_params']))
            self.mySimulator = Simulator(self.sim_params,cand_var,cell_var,self.bio_params['gate_params']).patch_clamp()

        mySimulator = self.mySimulator

        Vcost = 0
        tempCost = 0
        M = 0
        N = 0
        VClampSim_I_copy = list(copy.deepcopy(mySimulator['I']))

        for trace in self.sampleData['VClamp']['traces']:
            if 'vol' in trace:
                if trace['vol'] is None:
                    costList = list()
                    for index in range(0,len(VClampSim_I_copy)):
                        tempCost = self.cost([mySimulator['t'],VClampSim_I_copy[index]],[trace['t'],trace['I']])
                        costList.append(tempCost)
                    tempCost = min(costList)
                    indexTemp = costList.index(tempCost)
                    Vcost += tempCost
                    N += len(trace['t'])
                    M += 1
                    del VClampSim_I_copy[indexTemp]
                else:
                    index = int((self.sim_params['protocol_end'] - trace['vol']) / self.sim_params['protocol_steps'])
                    tempCost = self.cost([mySimulator['t'],mySimulator['I'][index]],[trace['t'],trace['I']])
                    Vcost += tempCost
                    N += len(trace['t'])
                    M += 1
            else:
                Vcost = self.cost_all_traces([mySimulator['t'],mySimulator['I']],[trace['t'],trace['I']])
                N = 1
                M = 1

            if (N * M) != 0:
                Vcost /= (N * M)

        if self.pso_flag and self.func != self.vclamp_cost:
            return self.V_dist - Vcost
        else:
            return Vcost

    def iclamp_cost(self,candidate):

        if 'IC' in self.sim_params:
            cand_var = dict(zip(self.bio_params['channel_params'],candidate))
            cell_var = dict(zip(self.bio_params['cell_params'],self.bio_params['val_cell_params']))
            self.mySimulator = Simulator(self.sim_params['IC'],cand_var,cell_var,self.bio_params['gate_params']).patch_clamp()
        elif (self.pso_flag and self.func == self.iclamp_cost) or self.mySimulator is None:
            cand_var = dict(zip(self.bio_params['channel_params'],candidate))
            cell_var = dict(zip(self.bio_params['cell_params'],self.bio_params['val_cell_params']))
            self.mySimulator = Simulator(self.sim_params,cand_var,cell_var,self.bio_params['gate_params']).patch_clamp()

        mySimulator = self.mySimulator

        tempCost = 0
        M = 0
        N = 0
        IClampSim_I_copy = list(copy.deepcopy(mySimulator['V']))

        Icost = 0

        for trace in self.sampleData['IClamp']['traces']:
            if 'amp' in trace:
               if trace['amp'] is None:
                    costList = list()
                    for index in range(0,len(IClampSim_I_copy)):
                        tempCost = self.cost([mySimulator['t'],IClampSim_I_copy[index]],[trace['t'],trace['V']])
                        costList.append(tempCost)
                    tempCost = min(costList)
                    indexTemp = costList.index(tempCost)
                    Icost += tempCost
                    N += len(trace['t'])
                    M += 1
                    del IClampSim_I_copy[indexTemp]
               else:
                    if 'IC' in self.sim_params:
                        index = int((trace['amp'] - self.sim_params['IC']['protocol_start']) / self.sim_params['IC']['protocol_steps'])
                    else:
                        index = int((trace['amp'] - self.sim_params['protocol_start']) / self.sim_params['protocol_steps'])
                    if mySimulator['V'][index]:
                        tempCost = self.cost([mySimulator['t'],mySimulator['V'][index]],[trace['t'],trace['V']])
                        Icost += tempCost
                        N += len(trace['t'])
                        M += 1
            else:
                Icost = self.cost_all_traces([mySimulator['t'],mySimulator['V']],[trace['t'],trace['V']])
                N = 1
                M = 1

        if (N * M) != 0:
            Icost /= (N * M)

        if self.pso_flag and self.func != self.iclamp_cost:
            return self.I_dist - Icost
        else:
            return Icost

    def iv_cost(self,candidate):

        if 'IV' in self.sim_params:
            cand_var = dict(zip(self.bio_params['channel_params'],candidate))
            cell_var = dict(zip(self.bio_params['cell_params'],self.bio_params['val_cell_params']))
            self.mySimulator = Simulator(self.sim_params['IV'],cand_var,cell_var,self.bio_params['gate_params']).patch_clamp()
        elif (self.pso_flag and self.func == self.iv_cost) or self.mySimulator is None:
            cand_var = dict(zip(self.bio_params['channel_params'],candidate))
            cell_var = dict(zip(self.bio_params['cell_params'],self.bio_params['val_cell_params']))
            self.mySimulator = Simulator(self.sim_params,cand_var,cell_var,self.bio_params['gate_params']).patch_clamp()

        mySimulator = self.mySimulator

        if 'I_peak' in self.sampleData['IV']:
            IVcost = self.cost([mySimulator['V_max'],mySimulator['I_max']],[self.sampleData['IV']['V'],self.sampleData['IV']['I_peak']])
        else:
            IVcost = self.cost([mySimulator['V_ss'],mySimulator['I_ss']],[self.sampleData['IV']['V'],self.sampleData['IV']['I']])
        N = len(self.sampleData['IV']['V'])
        if N != 0:
            IVcost /= N

        if self.pso_flag and self.func != self.iv_cost:
            return self.IV_dist - IVcost
        else:
            return IVcost

    def pov_cost(self,candidate):

        if 'POV' in self.sim_params:
            cand_var = dict(zip(self.bio_params['channel_params'],candidate))
            cell_var = dict(zip(self.bio_params['cell_params'],self.bio_params['val_cell_params']))
            self.mySimulator = Simulator(self.sim_params['POV'],cand_var,cell_var,self.bio_params['gate_params']).patch_clamp()
        elif (self.pso_flag and self.func == self.pov_cost) or self.mySimulator is None:
            cand_var = dict(zip(self.bio_params['channel_params'],candidate))
            cell_var = dict(zip(self.bio_params['cell_params'],self.bio_params['val_cell_params']))
            self.mySimulator = Simulator(self.sim_params,cand_var,cell_var,self.bio_params['gate_params']).patch_clamp()

        mySimulator = self.mySimulator
        if 'PO_peak' in self.sampleData['POV']:
            POVcost = self.cost([mySimulator['V_PO_max'],mySimulator['PO_max']],[self.sampleData['POV']['V'],self.sampleData['POV']['PO_peak']])
        else:
            POVcost = self.cost([mySimulator['V_ss'],mySimulator['PO_ss']],[self.sampleData['POV']['V'],self.sampleData['POV']['PO']])
        N = len(self.sampleData['POV']['V'])
        if N != 0:
            POVcost /= N

        if self.pso_flag and self.func != self.pov_cost:
            return self.POV_dist - POVcost
        else:
            return POVcost

    def cost(self, sim, target):
        """
        Gets simulation data and target data (experimental/digitazed) to calculate cost for each trace.
        Cost function calculation is based on Gurkiewicz & Korngreen approach (doi:10.1371/journal.pcbi.0030169.)
        The closest values in X-axis will be compared with corresponding values in Y-axis
        For scaling, the cost value will be divided by the mean value of the Y-axis in the target dataset.

        :param: sim: A 2D array of simulated data (one trace for I- or V- clamp)
        :param: target: A 2D array of experimental/digitized data
        :param: scale: if True, then scales the cost value by dividing by the sigma squared of the Y-axis in the target dataset.
        :return: cost_val: the cost value
        """
        # TODO: a better way to calculate cost is to measure the area between two plots!!

        sim_x = np.asarray(sim[0])
        total_cost = 1e9
        sum_var = 0
        x = np.asarray(target[0])
        y = np.asarray(target[1])

        if self.weight and set(x) == set(sim_x):
            # TODO: consider IC, IV, etc for sim_params
            on = self.sim_params['start_time']
            off = self.sim_params['end_time']
            onset = np.abs(x-on).argmin()
            offset = np.abs(x-off).argmin()
            peak = np.abs(y[onset+1:offset]).argmax() + onset+1
            tail = offset-1

        mu = np.mean(target[1])
        N=0

        for target_x in target[0]:
            index = np.abs(sim_x - target_x).argmin()

            if index < len(sim[1]):
                # if there is a comparable data and it's the first time, initialize the cost value with zero to calculate the total cost
                # else return a big number, to ignore this candidate

                if total_cost == 1e9: total_cost = 0
                sim_y = sim[1][index]
                target_i = target[0].index(target_x)
                target_y = target[1][target_i]
                cost_val = (target_y - sim_y)**2
                N+=1

                # considering weight
                if self.weight and set(x) == set(sim_x):
                    if target_y == target[1][0]:
                        cost_val *= self.weight['start']
                        N += self.weight['start']
                    elif target_y == target[1][-1]:
                        cost_val *= self.weight['end']
                        N += self.weight['end']
                    elif target_y ==  target[1][peak]:
                        cost_val *= self.weight['peak']
                        N += self.weight['peak']
                    elif target_y ==  target[1][tail]:
                        cost_val *= self.weight['tail']
                        N += self.weight['tail']
                    elif target_i in self.weight:
                        cost_val *= self.weight[target_i]
                        N += self.weight[target_i]

                # scale cost (for r-squared score)
                # http://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.linregress.html
                if self.scale:
                    var = ((target_y - mu)**2)
                    sum_var += var
                total_cost += cost_val

        if sum_var == 0:
            return total_cost
        else:
            return (total_cost/sum_var)

    def cost_all_traces(self, sim, target):
        """
        Gets simulation data and target data (experimental/digitazed) to calculate cost for all traces in one plot.

        :param: sim: Array of simulated experiment including all traces
        :param: terget: A 2D array of experimental/digitized data
        :param: scale: if True, then scales the cost value by dividing by the sigma squared of the Y-axis in the target dataset.
        :return: total_cost: the cost value
        """

        deltat = self.sim_params['deltat']
        numtests = int(round((self.sim_params['protocol_end'] - self.sim_params['protocol_start']) / self.sim_params['protocol_steps']) + 1)
        numpoints = int(round(self.sim_params['duration']/deltat))

        I = sim[1]
        target_temp = copy.deepcopy(target)
        min_dist = []
        t_sample = int(len(target_temp[0])/numtests)
        numsample = numpoints/t_sample
        # sigmasq = np.var(target[1])
        max = np.max(target[1])
        min = np.min(target[1])
        # y_scale = (min-max)**2

        for j in range(0,numtests):
            for i in range(1,numpoints):
                if i % int(numsample) == 0:
                    knn = nsmallest(numtests, target_temp[0], key=lambda x:abs(x-(i*deltat))**2)
                    knn_dist = list()
                    knn_dist.extend([[target_temp[0].index(k),(target_temp[1][target_temp[0].index(k)]-I[j][i])**2] for k in knn])
                    knn_dist = np.asarray(knn_dist)
                    knn_sort = knn_dist[knn_dist[:,1].argsort()]
                    knn_iy = int(knn_sort[0][0])
                    min_dist.append(knn_sort[0][1])

                    del target_temp[0][knn_iy]
                    del target_temp[1][knn_iy]

        total_cost = np.mean(min_dist)
        if self.scale:
            # total_cost /= sigmasq
            total_cost /= (((total_cost - max)**2 + (total_cost - min)**2)/2)
            # total_cost /= y_scale
            # if total_cost > 1: total_cost = 1

        return total_cost

    def pso_evaluate(self,lb,ub,args={}):
        """
        Optimization using Particle swarm optimization (PSO) algorithm.
        One function would be considered as the minimization function (with priority).
        Other cost functions, would be considered as constraints.
        All functions return mean squared distance between sample and simulated curves

        Optional inputs for pso:

        swarmsize : int
        The number of particles in the swarm (Default: 100)
        omega : scalar
        Particle velocity scaling factor (Default: 0.5)
        phip : scalar
        Scaling factor to search away from the particles best known position (Default: 0.5)
        phig : scalar
        Scaling factor to search away from the swarms best known position (Default: 0.5)
        maxiter : int
        The maximum number of iterations for the swarm to search (Default: 100)
        minstep : scalar
        The minimum stepsize of swarms best position before the search terminates (Default: 1e-8)
        minfunc : scalar
        The minimum change of swarms best objective value before the search terminates (Default: 1e-8)
        debug : boolean
        If True, progress statements will be displayed every iteration (Default: False)

        :param lb: Lower bound values
        :param ub: Upper bound values
        :param args: Optional arguments for pso function
        :return: optimized values
        """

        self.scale = False
        self.pso_flag = True
        self.func = self.vclamp_cost
        func_flag = False
        cons = list()

        # Initialize pso optional arguments
        if 'swarmsize' in args:
            swarmsize = args['swarmsize']
        else:
            swarmsize = 100
        if 'maxiter' in args:
            maxiter = args['maxiter']
        else:
            maxiter = 100
        if 'minstep' in args:
            minstep = args['minstep']
        else:
            minstep = 1e-8
        if 'minfunc' in args:
            minfunc = args['minfunc']
        else:
            minfunc = 1e-8
        if 'debug' in args:
            debug = args['debug']
        else:
            debug = False

        # Define minimum acceptable cost value for constrains
        if 'func' in args:
            self.func = args['func']
        else:
            self.func = self.vclamp_cost

        if 'IV_dist' in args:
            self.IV_dist = args['IV_dist']
        else:
            self.IV_dist = 1e-20

        if 'POV_dist' in args:
            self.POV_dist = args['POV_dist']
        else:
            self.POV_dist = 25e-4

        if 'I_dist' in args:
            self.I_dist = args['I_dist']
        else:
            self.I_dist = 1e-8

        if 'V_dist' in args:
            self.V_dist = args['V_dist']
        else:
            self.V_dist = 1e-20

        # Define minimization function and constraints
        if 'VClamp' in self.sampleData:
            self.func = self.vclamp_cost
            func_flag = True

        if 'IClamp' in self.sampleData:
            if func_flag == False:
                self.func = self.iclamp_cost
                func_flag = True
            else:
                cons.append(self.iclamp_cost)

        if 'IV' in self.sampleData:
            if func_flag == False:
                self.func = self.iv_cost
                func_flag = True
            else:
                cons.append(self.iv_cost)

        if 'POV' in self.sampleData:
            if func_flag == False:
                self.func = self.pov_cost
                func_flag = True
            else:
                cons.append(self.pov_cost)

        xopt, fopt = pso(func=self.func,
                         lb=lb,
                         ub=ub,
                         ieqcons=cons,
                         debug=debug,
                         swarmsize=swarmsize,
                         maxiter=maxiter,
                         minfunc=minfunc,
                         minstep=minstep)

        return xopt,fopt
