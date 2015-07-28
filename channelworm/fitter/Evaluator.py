import numpy as np
from channelworm.fitter.Simulator import Simulator
from heapq import nsmallest
import copy

class Evaluator(object):

    def __init__(self, sampleData, sim_params, bio_params):

        self.sampleData = sampleData
        self.sim_params = sim_params
        self.bio_params = bio_params

        if sim_params['pc_type'] == 'IClamp':
            self.steps = np.arange(sim_params['IC']['protocol_start'], sim_params['IC']['protocol_end'], sim_params['IC']['protocol_steps'])
        else:
            self.steps = np.arange(sim_params['protocol_start'], sim_params['protocol_end'], sim_params['protocol_steps'])

    def evaluate(self, candidates, args=[]):
        """
        Runs VClamp and/or IClamp simulation to calculate the cost value for each candidate.
        I/V curve is also considered as an evaluation factor and coming from VClamp or IClamp simulations.
        The approach is based on Gurkiewicz & Korngreen study (doi:10.1371/journal.pcbi.0030169.)

        :param: candidates: Candidate set from the GA that should be evaluated.
        :param: args: arguments if needed (based on Inspyred requirements for evaluate function)
        :return: total_fitness
        """

        # TODO: Include weights and minimization function (e.g. prAxis)
        # Based on Gurkiewicz & Korngreen approach (doi:10.1371/journal.pcbi.0030169.)

        fitness = 1e10
        total_fitness = []
        Vcost = 0
        Icost = 0
        IVcost = 0
        POVcost = 0

        for candidate in candidates:
            samples = 0
            cand_var = dict(zip(self.bio_params['channel_params'],candidate))
            cell_var = dict(zip(self.bio_params['cell_params'],self.bio_params['val_cell_params']))

            mySimulator = Simulator(self.sim_params,cand_var,cell_var).patch_clamp()

            if 'VClamp' in self.sampleData:

                tempCost = 0
                M = 0
                N = 0
                VClampSim_I_copy = list(copy.deepcopy(mySimulator['I']))

                for trace in self.sampleData['VClamp']['traces']:
                    if 'vol' in trace:
                        if trace['vol'] == None:
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
                            index = int((trace['vol'] - self.sim_params['protocol_start']) / self.sim_params['protocol_steps'])

                            if mySimulator['I'][index]:
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
                    samples += 1


            if 'IClamp' in self.sampleData:
                if 'IC' in self.sim_params:
                    mySimulator = Simulator(self.sim_params['IC'],cand_var,cell_var).patch_clamp()

                M = 0
                N = 0

                for trace in self.sampleData['IClamp']['traces']:
                    if 'amp' in trace:
                        index = int((trace['amp'] - self.sim_params['IC']['protocol_start']) / self.sim_params['IC']['protocol_steps'])
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
                    Icost  /= (N * M)
                samples += 1

            if 'IV' in self.sampleData:
                if 'IV' in self.sim_params:
                    mySimulator = Simulator(self.sim_params['IV'],cand_var,cell_var).patch_clamp()
                IVcost = self.cost([mySimulator['V_max'],mySimulator['I_max']],[self.sampleData['IV']['V'],self.sampleData['IV']['I']])
                N = len(self.sampleData['IV']['V'])
                if N != 0:
                    IVcost /= N
                samples += 1

            if 'POV' in self.sampleData:
                if 'POV' in self.sim_params:
                    mySimulator = Simulator(self.sim_params['POV'],cand_var,cell_var).patch_clamp()
                POVcost = self.cost([mySimulator['V_PO_max'],mySimulator['PO_max']],[self.sampleData['POV']['V'],self.sampleData['POV']['PO']])
                N = len(self.sampleData['POV']['V'])
                if N != 0:
                    POVcost /= N
                samples += 1

            fitness = (Vcost + Icost + IVcost + POVcost) / samples

            total_fitness.append(fitness)

        return total_fitness


    def cost(self, sim, target, scale=True):
        """
        Gets simulation data and target data (experimental/digitazed) to calculate cost for each trace.
        Cost function calculation is based on Gurkiewicz & Korngreen approach (doi:10.1371/journal.pcbi.0030169.)
        The closest values in X-axis will be compared with corresponding values in Y-axis
        For scaling, the cost value will be divided by the mean value of the Y-axis in the target dataset.

        :param: sim: A 2D array of simulated data (one trace for I- or V- clamp)
        :param: terget: A 2D array of experimental/digitized data
        :param: scale: if True, then scales the cost value by dividing by the sigma squared of the Y-axis in the target dataset.
        :return: cost_val: the cost value
        """
        # TODO: a better way to calculate cost is to measure the area between two plots!!

        sim_x = np.asarray(sim[0])
        total_cost = 1e9
        mu = np.mean(target[1])
        max = np.max(target[1])
        min = np.min(target[1])
        sigmasq = np.var(target[1])
        N=0

        for target_x in target[0]:
            index = np.abs(sim_x - target_x).argmin()

            if index < len(sim[1]):
                # if there is a comparable data and it's the first time, initialize the cost value with zero to calculate the total cost
                # else return a big number, to ignore this candidate

                if total_cost == 1e9: total_cost = 0
                sim_y = sim[1][index]
                target_y = target[1][target[0].index(target_x)]
                cost_val =  (target_y - sim_y)**2
                N+=1
                # scale distance
                if scale:
                    cost_val /= (((target_y - max)**2 + (target_y - min)**2)/2)

                total_cost += cost_val

        return total_cost

    def cost_all_traces(self, sim, target, scale=True):
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
        sigmasq = np.var(target[1])
        max = np.max(target[1])
        min = np.min(target[1])

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
        if scale:
            # total_cost /= sigmasq
            total_cost /= (((total_cost - max)**2 + (total_cost - min)**2)/2)

        return total_cost


    def patch_clamp_analysis(self,X,Y,type='VClamp'):
        """
        Analysis of a voltage- or current- clamp curve (usually digitized from figures)

        :param X: X axis, t
        :param Y: Y axis, V or I
        :param type: patch clamp type, VClamp, or IClamp
        :return: self.analysis: analysis key-vals
        """

        self.analysis = dict()

        # deltat = self.sim_params['deltat']
        onset = self.sim_params['start_time']
        offset = self.sim_params['end_time']

        # onset_i = X.index(min(X, key=lambda x:abs(x-onset)))
        # offset_i = X.index(min(X[offset:], key=lambda x:abs(x-offset)))
        peak_i = Y.index(max(abs(Y[onset:offset])))

        self.analysis['start'] = [X[0],Y[0]]
        self.analysis['end'] = [X[-1],Y[-1]]
        # self.analysis['onset'] = [onset,Y[0]]
        # self.analysis['offset'] = [offset,Y[offset_i]]
        self.analysis['peak'] = [X[peak_i],Y[peak_i]]

        half_a_i = Y.index(np.mean(Y[onset:peak_i]))
        self.analysis['v_half_a'] = [X[peak_i],Y[peak_i]]
        self.analysis['T_a'] = [X[peak_i],Y[peak_i]]
        self.analysis['k_a'] = [X[peak_i],Y[peak_i]]

        return self.analysis