import numpy as np

from cwFitter import Simulator


class Evaluator(object):

    def __init__(self, sampleData, sim_params, bio_params):

        self.sampleData = sampleData
        self.sim_params = sim_params
        self.bio_params = bio_params
        if 'protoco_start_I' in sim_params:
            self.steps = np.arange(sim_params['protocol_start_I'], sim_params['protocol_end_I'], sim_params['protocol_steps_I'])
        else:
            self.steps = np.arange(sim_params['protocol_start'], sim_params['protocol_end'], sim_params['protocol_steps'])

    def evaluate(self, candidates, args):
        """
        Runs VClamp and/or IClamp simulation to calculate the cost value for each candidate.
        I/V curve is also considered as an evaluation factor and coming from VClamp or IClamp simulations.
        The approach is based on Gurkiewicz & Korngreen study (doi:10.1371/journal.pcbi.0030169.)

        :return: total_cost
        """

        #TODO: Include weights and minimization function (e.g. prAxis)
        #Based on Gurkiewicz & Korngreen approach (doi:10.1371/journal.pcbi.0030169.)

        fitness = 1e10
        total_fitness = []
        Vcost = 0
        Icost = 0
        IVcost = 0
        IVFlag = False
        samples = 0

        for candidate in candidates:
            cand_var = dict(zip(self.bio_params['channel_params'],candidate))
            cell_var = dict(zip(self.bio_params['cell_params'],self.bio_params['val_cell_params']))

            mySimulator = Simulator.Simulator(self.sim_params,cand_var,cell_var)

            if ('VClamp' in self.sampleData) or (('IV' in self.sampleData) and (('VClamp' and 'IClamp') not in self.sampleData)):

                VClampSim_t,VClampSim_I,VClampSim_Vmax,VClampSim_Imax = mySimulator.VClamp()
                tempCost = 0
                M = 0
                N = 0

                if 'VClamp' in self.sampleData:

                    for trace in self.sampleData['VClamp']['traces']:
                        index = int((trace['vol'] - self.sim_params['protocol_start']) / self.sim_params['protocol_steps'])
                        if VClampSim_I[index] :
                            tempCost , N = self.cost([VClampSim_t,VClampSim_I[index]],[trace['t'],trace['I']])
                            Vcost += tempCost
                            N += N
                            M += 1

                    if (N * M) != 0:
                        Vcost /= (N * M)
                    samples += 1

                if 'IV' in self.sampleData:
                    IVcost , N = self.cost([VClampSim_Vmax,VClampSim_Imax],[self.sampleData['IV']['V'],self.sampleData['IV']['I']])
                    if N != 0:
                        IVcost /= N
                    IVFlag = True
                    samples += 1

            if 'IClamp' in self.sampleData:

                IClampSim_t,IClampSim_v,IClampSim_Vmax,IClampSim_Imax = mySimulator.IClamp()
                tempCost = 0
                M = 0
                N = 0

                for trace in self.sampleData['IClamp']['traces']:
                    index = int((trace['amp'] - self.sim_params['protocol_start_I']) / self.sim_params['protocol_steps_I'])
                    if IClampSim_v[index]:
                        tempCost , N = self.cost([IClampSim_t,IClampSim_v[index]],[trace['t'],trace['V']])
                        Icost += tempCost
                        N += N
                        M += 1

                if (N * M) != 0:
                    Icost  /= (N * M)
                samples += 1

                if IVFlag == False and 'IV' in self.sampleData:
                    IVcost , N = self.cost([IClampSim_Vmax,IClampSim_Imax],[self.sampleData['IV']['V'],self.sampleData['IV']['I']])
                    if N != 0:
                        IVcost /= N
                    IVFlag = True
                    samples += 1

            fitness = (Vcost + Icost + IVcost) / samples

            total_fitness.append(fitness)

        return total_fitness


    def cost(self, sim, target):
        """
        Get simulation data and target data (experimental/digitazed) to calculate cost.
        Cost function calculation is based on Gurkiewicz & Korngreen approach (doi:10.1371/journal.pcbi.0030169.)

        :return:
        """
        #TODO: a better way to calculate cost is to measure the area between two plots!!

        sim_x = sim[0]
        cost_val = 1e9
        N = 0

        for target_x in target[0]:
            index = sim_x.index(min(sim_x, key=lambda x:abs(x-target_x))) #TODO: check if the distance is in a reasonable range (consider a sigma)
            if sim[1][index]:
                #if there is a comparable data and it's the first time, initialize the cost value with zero to calculate the total cost
                #else return a big number, to ignore this candidate

                if cost_val == 1e9: cost_val = 0
                sim_y = sim[1][index]
                target_y = target[1][target[0].index(target_x)] #TODO: look for a better way to work with indices
                cost_val +=  (target_y - sim_y)**2 #TODO: normalize distance
                N += 1

        return cost_val , N


