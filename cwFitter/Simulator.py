import numpy as np
import matplotlib.pyplot as plt
from math import exp

class Simulator(object):

    def __init__(self, sim_params, channel_params, cell_params):

        # Simulation Parameters
        self.sim_params = sim_params
        self.ion_type = sim_params['ion_type']
        self.v_init = sim_params['v_init']
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

        #Channel parameters
        self.c_mem = cell_params['C_mem']
        # if 'g_cap' in channel_params:
        #     self.g = channel_params['g_cap'] * cell_params['C_mem']
        # elif 'g_dens' in channel_params:
        #     self.g = channel_params['g_dens'] * cell_params['C_mem'] / cell_params['spec_cap']
        # else:
        self.g = channel_params['g']
        self.e_rev = channel_params['e_rev']
        self.v_half_a = channel_params['v_half_a']
        self.v_half_i = channel_params['v_half_i']
        self.k_a = channel_params['k_a']
        self.k_i = channel_params['k_i']
        self.T_a = channel_params['T_a']
        self.T_i = channel_params['T_i']
        self.a_power = int(channel_params['a_power'])
        self.i_power = int(channel_params['i_power'])

        if self.ion_type == 'Ca':
            self.Ca = list()
            self.cdi = list()
            self.ca_half_i = channel_params['ca_half_i']
            self.k_ca = channel_params['k_ca']
            self.T_ca = channel_params['T_ca']
            self.alpha_ca = channel_params['alpha_ca']
            self.cdi_power = int(channel_params['cdi_power'])

            self.ca_con = cell_params['ca_con']
            self.thi_ca = self.ca_con/(self.T_ca * self.g)

        #TODO: change declaration with np.zeros((n,numtests))
        # Variable Declaration        
        self.V = list()
        self.I = list()
        self.V_max = list()
        self.I_max = list()
        self.I_mem = list()
        self.I_in = list()
        self.act = list()
        self.inact = list()


    def boltzmannFit(self,V,Vhalf,k):

        # Preventing exp() overflow error
        #if -708 < (Vhalf - V)/k < 708:
        try:
            return 1/(1 + exp((Vhalf - V)/k))
        except:
            if (Vhalf - V)/k > 0:
                return 0
            else:
                return 1


    def VClamp(self):
        """
        Simulates a voltage clamp experiment.

        :return: time vector and corresponding current values, also maximum values for I and V in each trace for plotting I/V
        """


        # Input initialization
        for i in range(0,self.numtests):
            self.V.append(list())
            self.I_mem.append(list())
            self.I_in.append(list())
            self.act.append(0)
            self.inact.append(0)
            self.I.append(0)
            self.I_max.append(0)
            self.V_max.append(0)
            if self.ion_type == 'Ca':
                self.Ca.append(list())
                self.cdi.append(0)
            for j in range(0,self.numpoints):
                self.V[i].append(0)
                self.I_mem[i].append(0)
                self.I_in[i].append(0)
                if self.ion_type == 'Ca':
                    self.Ca[i].append(0)

        for i in range(0,self.numtests):
            for j in range(0,self.numpoints):
                self.V[i][j] = self.v_init

        self.Vstim = self.protocol_end
        for i in range(0,self.numtests):
            for j in range(self.onset-1,self.offset):
                self.V[i][j] = self.Vstim
            self.Vstim = self.Vstim - self.protocol_steps

        # Variable initialization
        for j in range(0,self.numtests):
            self.Ca[j][0] = 0
            self.act[j] = self.boltzmannFit(self.V[j][0], self.v_half_a, self.k_a)
            self.inact[j] = self.boltzmannFit(self.V[j][0], self.v_half_i, self.k_i)
            self.cdi[j] = self.boltzmannFit(self.V[j][0], self.ca_half_i, self.k_ca)

        # Start of simulation
        for j in range(0,self.numtests):
            for i in range(1,self.numpoints):
                da = (self.boltzmannFit(self.V[j][i-1], self.v_half_a, self.k_a) - self.act[j])/self.T_a
                self.act[j] = self.act[j] + da*self.deltat
                di = (self.boltzmannFit(self.V[j][i-1], self.v_half_i, self.k_i) - self.inact[j])/self.T_i
                self.inact[j] = self.inact[j] + di*self.deltat

                self.I = self.g * self.act[j]**self.a_power * self.inact[j]**self.i_power * (self.V[j][i-1] - self.e_rev)

                if self.ion_type == 'Ca':
                    self.cdi[j] = self.boltzmannFit(self.Ca[j][i-1], self.ca_half_i, self.k_ca)
                    self.I *= (1 + (self.cdi[j] - 1) * self.alpha_ca)**self.cdi_power

                    self.dCa = -(self.Ca[j][i-1] / self.T_ca + self.thi_ca * self.I)
                    self.Ca[j][i] = self.Ca[j][i-1] + self.dCa * self.deltat

                self.I_mem[j][i] = self.I

                if (self.onset < i < self.offset):
                    if abs(self.I) > abs(self.I_max[j]):
                        self.I_max[j] = self.I
                        self.V_max[j] = self.V[j][i]

        #     plt.plot(self.xaxis, [x * 1e9 for x in self.I_mem[j]])
        #
        # plt.ylabel('Imem (nA)')
        # plt.xlabel('Time (ms)')
        # plt.show()

        return self.xaxis,self.I_mem,self.V_max,self.I_max


    def IClamp(self):
        """
        Simulates a current clamp experiment.

        :return: time vector and corresponding voltage values, also maximum values for I and V in each trace for plotting I/V
        """

        # Input initialization
        ion_type = self.sim_params['ion_type_I']
        v_init = self.sim_params['v_init_I']
        deltat = self.sim_params['deltat_I']
        duration = self.sim_params['duration_I']
        numpoints = int(round(duration/deltat))
        protocol_start = self.sim_params['protocol_start_I']
        protocol_end = self.sim_params['protocol_end_I']
        protocol_steps = self.sim_params['protocol_steps_I']
        numtests = int(round((self.sim_params['protocol_end_I'] - self.sim_params['protocol_start_I']) / self.sim_params['protocol_steps_I']) + 1)
        xaxis = [float(x) for x in np.arange(deltat, duration + deltat, deltat)]
        onset = int(round(self.sim_params['start_time_I']/deltat))
        offset = int(round(self.sim_params['end_time_I']/deltat))

        for i in range(0,numtests):
            self.V.append(list())
            self.I_mem.append(list())
            self.I_in.append(list())
            self.act.append(0)
            self.inact.append(0)
            self.I.append(0)
            self.I_max.append(0)
            self.V_max.append(0)
            if self.ion_type == 'Ca':
                self.Ca.append(list())
                self.cdi.append(0)
            for j in range(0,self.numpoints):
                self.V[i].append(0)
                self.I_mem[i].append(0)
                self.I_in[i].append(0)
                if self.ion_type == 'Ca':
                    self.Ca[i].append(0)

        for i in range(0,numtests):
            for j in range(0,numpoints):
                self.I_in[i][j] = 0

        self.Istim = -protocol_start
        for i in range(0,numtests):
            for j in range(onset-1,offset):
                self.I_in[i][j] = self.I_in[i][j] + self.Istim
            self.Istim = self.Istim - protocol_steps

        # Variable initialization
        for j in range(0,numtests):
            self.V[j][0] = v_init
            self.Ca[j][0] = 0
            self.act[j] = self.boltzmannFit(self.V[j][0], self.v_half_a, self.k_a)
            self.inact[j] = self.boltzmannFit(self.V[j][0], self.v_half_i, self.k_i)
            self.cdi[j] = self.boltzmannFit(self.V[j][0], self.ca_half_i, self.k_ca)

        # Start of simulation
        for j in range(0,numtests):
            for i in range(1,numpoints):
                da = (self.boltzmannFit(self.V[j][i-1], self.v_half_a, self.k_a) - self.act[j])/self.T_a
                self.act[j] = self.act[j] + da*deltat
                di = (self.boltzmannFit(self.V[j][i-1], self.v_half_i, self.k_i) - self.inact[j])/self.T_i
                self.inact[j] = self.inact[j] + di*deltat

                self.I = self.g * self.act[j]**self.a_power * self.inact[j]**self.i_power * (self.V[j][i-1] - self.e_rev)

                if ion_type == 'Ca':
                    self.cdi[j] = self.boltzmannFit(self.Ca[j][i-1], self.ca_half_i, self.k_ca)
                    self.I *= (1 + (self.cdi[j] - 1) * self.alpha_ca)**self.cdi_power

                    self.dCa = -(self.Ca[j][i-1] / self.T_ca + self.thi_ca * self.I)
                    self.Ca[j][i] = self.Ca[j][i-1] + self.dCa * deltat


                dv = -(self.I_in[j][i] + self.I)
                self.V[j][i] = self.V[j][i-1] + dv * deltat

                if (onset < i < offset):
                    if abs(self.I) > abs(self.I_max[j]):
                        self.I_max[j] = self.I
                        self.V_max[j] = self.V[j][i]

        #     plt.plot(self.xaxis, [x * 1 for x in self.V[j]])
        #
        # plt.ylabel('V (mv)')
        # plt.xlabel('Time (ms)')
        # plt.show()

        return xaxis,self.V,self.V_max,self.I_max


    def IV(self,v_range,ca_range=[],units={'I':'A','V':'V'},plot=False):
        """
        Calculates current for a given voltage.

        :param v_range: voltage vector including V points
        :param ca_range: in case of Calcium ion channel, we would need the [Ca2+] range
        :param units: dictionary of units for converting. current unit can be A, A/F, or pA, and voltage unit V, and mV
        :param plot: if set to True, plot will be showed
        :return: Current vector
        """

        V = v_range
        Ca = ca_range

        numpoints = len(V)
        I = np.zeros(numpoints)

        for i in range(0,numpoints):
            I[i] = self.g * self.boltzmannFit(V[i], self.v_half_a, self.k_a)**self.a_power * self.boltzmannFit(V[i], self.v_half_i, self.k_i)**self.i_power * (V[i] - self.e_rev)

            if len(Ca) > 0:
                I[i] *= (1 + self.boltzmannFit(Ca[i], self.ca_half_i, self.k_ca) - 1) * self.alpha_ca**self.cdi_power


        if plot == True:

            if units['I'] == 'A/F':
                for i in I: I[i] /= self.c_mem
            elif units['I'] == 'pA':
                for i in I: I[i] *= 1e12
            if units['V'] == 'mV':
                for i in V: V[i] *= 1e3


            plt.plot(V,I, label='Current vs Voltage')
            plt.ylabel('I (%s)'%(units['I']))
            plt.xlabel('V (%s)'%(units['V']))
            plt.grid('on')

            plt.show()

        return I

