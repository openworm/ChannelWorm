import numpy as np
import matplotlib.pyplot as plt
from math import exp
from scipy.optimize import curve_fit

class Simulator(object):

    def __init__(self, sim_params, channel_params, cell_params):

        self.sim_params = sim_params
        self.channel_params = channel_params
        self.cell_params = cell_params

        # Simulation Parameters
        self.pc_type = sim_params['pc_type']
        self.v_hold = sim_params['v_hold']
        self.I_init = sim_params['I_init']
        self.deltat = sim_params['deltat']
        self.duration = sim_params['duration']
        self.numpoints = int(round(self.duration/self.deltat))
        self.protocol_start = sim_params['protocol_start']
        self.protocol_end = sim_params['protocol_end']
        self.protocol_steps = sim_params['protocol_steps']
        self.numtests = int(round((sim_params['protocol_end'] - sim_params['protocol_start']) / sim_params['protocol_steps']) + 1)
        self.xaxis = [float(x) for x in np.arange(self.deltat, self.duration + self.deltat, self.deltat)]
        self.onset = int(round(sim_params['start_time']/self.deltat))
        self.offset = int(round(sim_params['end_time']/self.deltat))
        self.gates = sim_params['gates']

        # Channel and cell parameters
        if 'C_mem' in cell_params:
            self.c_mem = cell_params['C_mem']
            if 'g_cap' in channel_params:
                self.g = channel_params['g_cap'] * self.c_mem
            elif ('g_dens' in channel_params) and ('spec_cap' in cell_params):
                self.g = channel_params['g_dens'] * self.c_mem / cell_params['spec_cap']
        else:
            self.g = channel_params['g']

        self.e_rev = channel_params['e_rev']

        # Gate parameters
        if 'vda' in self.gates:
            self.v_half_a = channel_params['v_half_a']
            self.k_a = channel_params['k_a']
            self.T_a = channel_params['T_a']
            self.a_power = int(channel_params['a_power'])

        if 'vdi' in self.gates:
            self.v_half_i = channel_params['v_half_i']
            self.k_i = channel_params['k_i']
            self.T_i = channel_params['T_i']
            self.i_power = int(channel_params['i_power'])

        if 'cdi' in self.gates:
            self.ca_half_i = channel_params['ca_half_i']
            self.k_ca = channel_params['k_ca']
            self.T_ca = channel_params['T_ca']
            self.alpha_ca = channel_params['alpha_ca']
            self.cdi_power = int(channel_params['cdi_power'])

            self.ca_con = sim_params['ca_con']
            self.thi_ca = self.ca_con/(self.T_ca * self.g)


    def boltzmannFit(self,x,mu,k):

        # Preventing exp() overflow error
        # if -708 < (mu - x)/k < 708:
        try:
            return 1/(1 + exp((mu - x)/k))
        except:
            if (mu - x)/k > 0:
                return 0
            else:
                return 1


    def IV_act(self,V,*args):

        self.zparams = dict(zip(self.fit_params,args))
        I_act = self.zparams['g_cap']*self.c_mem * (1/(1 + np.exp((self.zparams['v_half_a'] - V)/self.zparams['k_a'])))**int(self.zparams['a_power']) * (V - self.zparams['e_rev'])
        return I_act


    def patch_clamp(self, t=[]):
        """
        Simulates a patch clamp experiment.

        :return: Corresponding values in a dict
        """

        self.results = dict()

        if len(t) > 0:
            self.xaxis = t
            self.onset = t[0]
            self.offset = t[-1]


        # Variable Declaration
        V = np.zeros((self.numtests,self.numpoints))
        I_mem = np.zeros((self.numtests,self.numpoints))
        I_in = np.zeros((self.numtests,self.numpoints))
        PO = np.zeros((self.numtests,self.numpoints))

        I_max = np.zeros(self.numtests)
        V_max = np.zeros(self.numtests)
        PO_max = np.zeros(self.numtests)
        V_PO_max = np.zeros(self.numtests)

        if 'vda' in self.gates:
            act = np.zeros((self.numtests,self.numpoints))
            act_max = np.zeros(self.numtests)
        if 'vdi' in self.gates:
            inact = np.zeros((self.numtests,self.numpoints))
            inact_max = np.zeros(self.numtests)
        if 'cdi' in self.gates:
            Ca = np.zeros((self.numtests,self.numpoints))
            cdi = np.zeros((self.numtests,self.numpoints))
            cdi_max = np.zeros(self.numtests)


        for i in range(0,self.numtests):
            for j in range(0,self.numpoints):
                V[i][j] = self.v_hold

        Vstim = self.protocol_end
        for i in range(0,self.numtests):
            for j in range(self.onset-1,self.offset):
                V[i][j] = Vstim
            Vstim -= self.protocol_steps


        if self.pc_type == 'IClamp':
            for i in range(0,self.numtests):
                for j in range(0,self.numpoints):
                    I_in[i][j] = self.I_init

            Istim = -self.protocol_start
            for i in range(0,self.numtests):
                for j in range(self.onset-1,self.offset):
                    I_in[i][j] += Istim
                Istim -= self.protocol_steps

        # Variable initialization
        for j in range(0,self.numtests):
            if 'vda' in self.gates:
                act[j][0] = self.boltzmannFit(V[j][0], self.v_half_a, self.k_a)
            if 'vdi' in self.gates:
                inact[j][0] = self.boltzmannFit(V[j][0], self.v_half_i, self.k_i)

        # Start of simulation
        for j in range(0,self.numtests):
            for i in range(1,self.numpoints):
                I = self.g * (V[j][i-1] - self.e_rev)
                po = 1

                if 'vda' in self.gates:
                    da = (self.boltzmannFit(V[j][i-1], self.v_half_a, self.k_a) - act[j][0])/self.T_a
                    act[j][0] += da*self.deltat
                    act[j][i] = act[j][0]**self.a_power
                    po *= act[j][i]

                if 'vdi' in self.gates:
                    di = (self.boltzmannFit(V[j][i-1], self.v_half_i, self.k_i) - inact[j][0])/self.T_i
                    inact[j][0] += di*self.deltat
                    inact[j][i] = inact[j][0]**self.i_power
                    po *= inact[j][i]

                if 'cdi' in self.gates:
                    cdi_b = self.boltzmannFit(Ca[j][i-1], self.ca_half_i, self.k_ca)
                    cdi[j][i] = (1 + (cdi_b - 1) * self.alpha_ca)**self.cdi_power
                    po *= cdi[j][i]

                    dCa = -(Ca[j][i-1] / self.T_ca + self.thi_ca * I)
                    Ca[j][i] = Ca[j][i-1] + dCa * self.deltat

                PO[j][i] = po
                I_mem[j][i] = I * po

                if self.pc_type == 'IClamp':
                    dv = -(I_in[j][i] + I) / self.c_mem
                    V[j][i] = V[j][i-1] + dv * self.deltat

                if (self.onset < i < self.offset):
                    if abs(I_mem[j][i]) > abs(I_max[j]):
                        I_max[j] = I_mem[j][i]
                        V_max[j] = V[j][i]
                    if po > PO_max[j]:
                        PO_max[j] = po
                        V_PO_max[j] = V[j][i]

        self.results['t'] = self.xaxis
        self.results['V'] = V
        self.results['I'] = I_mem
        self.results['V_max'] = V_max
        self.results['I_max'] = I_max
        self.results['PO'] = PO
        self.results['PO_max'] = PO_max
        self.results['V_PO_max'] = V_PO_max
        if 'vda' in self.gates:
            self.results['act'] = act
        if 'vdi' in self.gates:
            self.results['inact'] = inact
        if 'cdi' in self.gates:
            self.results['Ca'] = Ca
            self.results['cdi'] = cdi


        if len(t) > 0:
            if self.pc_type == 'IClamp':
                return V
            else:
                return I_mem
        else:
            return self.results


    def optim_curve(self, params, best_candidate, target, curve_type='IV'):

        self.target = target
        X = np.asarray(target[0])
        Y = np.asarray(target[1])

        # in scipy leastsq, number of parameters must not exceed number of points.
        diff = len(best_candidate) - len(X)
        if diff > 0:
            for i in range(0,diff):
                X = np.append(X,X[-1])
                Y = np.append(Y,Y[-1])

        self.fit_params = params
        if curve_type == 'IV':
            popt,pcov = curve_fit(self.IV_act, X,Y,best_candidate)

        return popt, self.zparams
