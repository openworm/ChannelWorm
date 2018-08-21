"""
ChannelWorm fitter module for simulating patch clamp experiments and generating related curves.
"""

import numpy as np
import matplotlib.pyplot as plt
from math import exp
from scipy.optimize import curve_fit, leastsq

class Simulator(object):

    def __init__(self, sim_params, channel_params, cell_params, gate_params, act_fit=False, pov_fit=False):

        self.sim_params = sim_params
        self.channel_params = channel_params
        self.cell_params = cell_params
        self.gates = gate_params
        self.act_fit = act_fit
        self.pov_fit = pov_fit

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

        # Channel and cell parameters
        # self.I_leak = cell_params['I_leak']
        if 'C_mem' in cell_params:
            self.c_mem = cell_params['C_mem']
        if 'g_cap' in channel_params:
            self.g = channel_params['g_cap'] * self.c_mem
        elif ('g_dens' in channel_params) and ('spec_cap' in cell_params):
            self.g = channel_params['g_dens'] * self.c_mem / cell_params['spec_cap']
        else:
            self.g = channel_params['g']

        self.e_rev = channel_params['e_rev']

        if 'gL' in channel_params:
            self.gL = channel_params['gL']

            if 'g_cap' in channel_params:
                self.gL *= self.c_mem
            elif ('g_dens' in channel_params) and ('spec_cap' in cell_params):
                self.gL *= (self.c_mem / cell_params['spec_cap'])

            self.VL = channel_params['VL']

        # Gate parameters
        if 'vda' in self.gates:
            self.v_half_a = channel_params['v_half_a']
            self.k_a = channel_params['k_a']
            if 'mtau' not in self.gates:
                self.T_a = channel_params['T_a']
            self.a_power = int(self.gates['vda']['power'])
            if 'rate_a' in channel_params:
                self.rate_a = channel_params['rate_a']
            else:
                self.rate_a = 1
            if 'C_a' in channel_params:
                self.C_a = channel_params['C_a']
            else:
                self.C_a = 1-self.rate_a

        if 'vdi' in self.gates:
            self.v_half_i = channel_params['v_half_i']
            self.k_i = channel_params['k_i']
            self.i_power = int(self.gates['vdi']['power'])
            if 'htau' not in self.gates:
                self.T_i = channel_params['T_i']
            if 'rate_i' in channel_params:
                self.rate_i = channel_params['rate_i']
            else:
                self.rate_i = 1
            if 'C_i' in channel_params:
                self.C_i = channel_params['C_i']
            else:
                self.C_i = 1-self.rate_i

        if 'cd' in self.gates:
            self.ca_half = channel_params['ca_half']
            self.k_ca = channel_params['k_ca']
            self.T_ca = channel_params['T_ca']
            self.alpha_ca = channel_params['alpha_ca']
            self.cd_power = int(self.gates['cd']['power'])

            self.ca_con = sim_params['ca_con']
            self.thi_ca = self.ca_con/(self.T_ca * self.g)

        if 'mtau' in self.gates:
            self.v_half_mt = channel_params['v_half_mt']
            self.k_mt = channel_params['k_mt']
            self.rate_mt = channel_params['rate_mt']
            self.mt_power = int(self.gates['mtau']['power'])
            if 'C_mt' in channel_params:
                self.C_mt = channel_params['C_mt']
            else:
                self.C_mt = 0

        if 'htau' in self.gates:
            self.v_half_ht = channel_params['v_half_ht']
            self.k_ht = channel_params['k_ht']
            self.rate_ht = channel_params['rate_ht']
            self.ht_power = int(self.gates['htau']['power'])
            if 'C_ht' in channel_params:
                self.C_ht = channel_params['C_ht']
            else:
                self.C_ht = 0

        if 'm' in self.gates:
            if 'v_half_m_a' in channel_params:
                self.v_half_m_a = channel_params['v_half_m_a']
            else:
                self.v_half_m_a = 1
            if 'v_half_m_b' in channel_params:
                self.v_half_m_b = channel_params['v_half_m_b']
            else:
                self.v_half_m_b = 1
            if 'k_m_a' in channel_params:
                self.k_m_a = channel_params['k_m_a']
            else:
                self.k_m_a = 1
            if 'k_m_b' in channel_params:
                self.k_m_b = channel_params['k_m_b']
            else:
                self.k_m_b = 1

            if 'rate_m_a' in gate_params['m']:
                self.rate_m_a = gate_params['m']['rate_m_a']
            elif 'rate_m_a' in channel_params:
                self.rate_m_a = channel_params['rate_m_a']
            else:
                self.rate_m_a = 1  
            if 'rate_m_b' in gate_params['m']:
                self.rate_m_b = gate_params['m']['rate_m_b']            
            elif 'rate_m_b' in channel_params:
                self.rate_m_b = channel_params['rate_m_b']
            else:
                self.rate_m_b = 1

            if 'power' in gate_params['m']:
                self.m_power = int(gate_params['m']['power'])
            elif 'm_power' in channel_params:
                self.m_power = int(channel_params['m_power'])
            else:
                self.m_power = 1
                
            if 'a_m_a' in gate_params['m']:
                self.a_m_a = int(gate_params['m']['a_m_a'])                
            elif 'a_m_a' in channel_params:
                self.a_m_a = int(channel_params['a_m_a'])
            else:
                self.a_m_a = 1
            if 'a_m_b' in gate_params['m']:
                self.a_m_b = int(gate_params['m']['a_m_b'])            
            elif 'a_m_b' in channel_params:
                self.a_m_b = int(channel_params['a_m_b'])
            else:
                self.a_m_b = 1
            if 'b_m_a' in gate_params['m']:
                self.b_m_a = int(gate_params['m']['b_m_a'])            
            elif 'b_m_a' in channel_params:
                self.b_m_a = int(channel_params['b_m_a'])
            else:
                self.b_m_a = 1
            if 'b_m_b' in gate_params['m']:
                self.b_m_b = int(gate_params['m']['b_m_b'])            
            elif 'b_m_b' in channel_params:
                self.b_m_b = int(channel_params['b_m_b'])
            else:
                self.b_m_b = 1
            if 'c_m_a' in gate_params['m']:
                self.c_m_a = int(gate_params['m']['c_m_a'])            
            elif 'c_m_a' in channel_params:
                self.c_m_a = int(channel_params['c_m_a'])
            else:
                self.c_m_a = 1
            if 'c_m_b' in gate_params['m']:
                self.c_m_b = int(gate_params['m']['c_m_b'])            
            elif 'c_m_b' in channel_params:
                self.c_m_b = int(channel_params['c_m_b'])
            else:
                self.c_m_b = 1
            if 'd_m_a' in gate_params['m']:
                self.d_m_a = int(gate_params['m']['d_m_a'])            
            elif 'd_m_a' in channel_params:
                self.d_m_a = int(channel_params['d_m_a'])
            else:
                self.d_m_a = 1
            if 'd_m_b' in gate_params['m']:
                self.d_m_b = int(gate_params['m']['d_m_b'])            
            elif 'd_m_b' in channel_params:
                self.d_m_b = int(channel_params['d_m_b'])
            else:
                self.d_m_b = 1
                 
        if 'h' in self.gates:
            if 'v_half_h_a' in channel_params:
                self.v_half_h_a = channel_params['v_half_h_a']
            else:
                self.v_half_h_a = 1
            if 'v_half_h_b' in channel_params:
                self.v_half_h_b = channel_params['v_half_h_b']
            else:
                self.v_half_h_b = 1
            if 'k_h_a' in channel_params:
                self.k_h_a = channel_params['k_h_a']
            else:
                self.k_h_a = 1
            if 'k_h_b' in channel_params:
                self.k_h_b = channel_params['k_h_b']
            else:
                self.k_h_b = 1

            if 'rate_h_a' in gate_params['h']:
                self.rate_h_a = gate_params['h']['rate_h_a']
            elif 'rate_h_a' in channel_params:
                self.rate_h_a = channel_params['rate_h_a']
            else:
                self.rate_h_a = 1  
            if 'rate_h_b' in gate_params['h']:
                self.rate_h_b = gate_params['h']['rate_h_b']            
            elif 'rate_h_b' in channel_params:
                self.rate_h_b = channel_params['rate_h_b']
            else:
                self.rate_h_b = 1                
                
            if 'power' in gate_params['h']:
                self.h_power = int(gate_params['h']['power'])
            elif 'h_power' in channel_params:
                self.h_power = int(channel_params['h_power'])
            else:
                self.h_power = 1
                
            if 'a_h_a' in gate_params['h']:
                self.a_h_a = int(gate_params['h']['a_h_a'])                
            elif 'a_h_a' in channel_params:
                self.a_h_a = int(channel_params['a_h_a'])
            else:
                self.a_h_a = 1
            if 'a_h_b' in gate_params['h']:
                self.a_h_b = int(gate_params['h']['a_h_b'])            
            elif 'a_h_b' in channel_params:
                self.a_h_b = int(channel_params['a_h_b'])
            else:
                self.a_h_b = 1
            if 'b_h_a' in gate_params['h']:
                self.b_h_a = int(gate_params['h']['b_h_a'])            
            elif 'b_h_a' in channel_params:
                self.b_h_a = int(channel_params['b_h_a'])
            else:
                self.b_h_a = 1
            if 'b_h_b' in gate_params['h']:
                self.b_h_b = int(gate_params['h']['b_h_b'])            
            elif 'b_h_b' in channel_params:
                self.b_h_b = int(channel_params['b_h_b'])
            else:
                self.b_h_b = 1
            if 'c_h_a' in gate_params['h']:
                self.c_h_a = int(gate_params['h']['c_h_a'])            
            elif 'c_h_a' in channel_params:
                self.c_h_a = int(channel_params['c_h_a'])
            else:
                self.c_h_a = 1
            if 'c_h_b' in gate_params['h']:
                self.c_h_b = int(gate_params['h']['c_h_b'])            
            elif 'c_h_b' in channel_params:
                self.c_h_b = int(channel_params['c_h_b'])
            else:
                self.c_h_b = 1
            if 'd_h_a' in gate_params['h']:
                self.d_h_a = int(gate_params['h']['d_h_a'])            
            elif 'd_h_a' in channel_params:
                self.d_h_a = int(channel_params['d_h_a'])
            else:
                self.d_h_a = 1
            if 'd_h_b' in gate_params['h']:
                self.d_h_b = int(gate_params['h']['d_h_b'])            
            elif 'd_h_b' in channel_params:
                self.d_h_b = int(channel_params['d_h_b'])
            else:
                self.d_h_b = 1

    def boltzmannFit(self, x, mu, k, a=1, c=0):

        # Preventing exp() overflow error
        # if -708 < (mu - x)/k < 708:
        try:
            return (a/(1 + exp((mu - x)/k))) + c
        except OverflowError:
            if (mu - x)/k > 0:
                return 1e-100 + c
            else:
                return a + c

    def alphaBetaFit(self,V,mu,k,rate=1,a=1,b=1,c=1,d=1):

        if k == 0:
            k = 1e-10
        x = np.divide((V-mu),k)

        if b==0 and c==0:
            return (rate*(a or x))
        else:

            # Preventing exp() overflow error
            # if -708 < (V+mu)/k < 708:
            try:
                return (rate*(a or x))/(b+(c*np.exp(-d*x)))
                # return (a+(b*V))/(c + h*exp((V+mu)/k))
            except ZeroDivisionError:
                return 0
            except OverflowError:
                if (-d*x) > 0:
                    return 0
                else:
                    if b == 0:
                        return 0
                    else:
                        return (rate*(a or x))/b

    def patch_clamp(self, t=[], *args):
        """
        Simulates a patch clamp experiment.

        :return: Corresponding values in a dict
        """

        self.results = dict()

        if len(args)>0:
            if len(args) == 1:
                args = args[0]
            self.channel_params = dict(zip(self.fit_params,args))
            self.zparams = self.channel_params
            self.__init__(self.sim_params, self.channel_params, self.cell_params, self.gates)

        # Variable Declaration
        V = np.zeros((self.numtests,self.numpoints))
        V.fill(self.v_hold)
        I_mem = np.zeros((self.numtests,self.numpoints))
        I_in = np.zeros((self.numtests,self.numpoints))
        PO = np.zeros((self.numtests,self.numpoints))

        I_max = np.zeros(self.numtests)
        I_ss = np.zeros(self.numtests)
        V_max = np.zeros(self.numtests)
        V_ss = np.zeros(self.numtests)
        PO_max = np.zeros(self.numtests)
        V_PO_max = np.zeros(self.numtests)

        if 'vda' in self.gates:
            act = np.zeros((self.numtests,self.numpoints))
            m_inf = np.zeros(self.numtests)
            m_inf_hold = self.boltzmannFit(self.v_hold, self.v_half_a, self.k_a, self.rate_a, self.C_a)
            m = m_inf_hold
            T_a = np.zeros(self.numtests)
            # act_max = np.zeros(self.numtests)
        if 'vdi' in self.gates:
            inact = np.zeros((self.numtests,self.numpoints))
            h_inf = np.zeros(self.numtests)
            h_inf_hold = self.boltzmannFit(self.v_hold, self.v_half_i, self.k_i, self.rate_i, self.C_i)
            h = h_inf_hold
            T_i = np.zeros(self.numtests)
            # inact_max = np.zeros(self.numtests)
        if 'cd' in self.gates:
            Ca = np.zeros((self.numtests,self.numpoints))
            cd = np.zeros((self.numtests,self.numpoints))
            cd_inf = np.zeros((self.numtests,self.numpoints))
            # cd_max = np.zeros(self.numtests)
        if 'm' in self.gates:
            act = np.zeros((self.numtests,self.numpoints))
            m_tau = np.zeros((self.numtests,self.numpoints))
            m_inf = np.zeros(self.numtests)
            alpha_m = np.zeros(self.numtests)
            beta_m = np.zeros(self.numtests)
            tau_m = np.zeros(self.numtests)
            alpha_m_hold = self.alphaBetaFit(self.v_hold, self.v_half_m_a, self.k_m_a, self.rate_m_a, self.a_m_a,self.b_m_a,self.c_m_a,self.d_m_a)
            beta_m_hold = self.alphaBetaFit(self.v_hold, self.v_half_m_b, self.k_m_b, self.rate_m_b, self.a_m_b,self.b_m_b,self.c_m_b,self.d_m_b)
            if (alpha_m_hold + beta_m_hold) != 0:
                m_inf_hold = alpha_m_hold / (alpha_m_hold + beta_m_hold)
            else:
                m_inf_hold = 0
            m = m_inf_hold
        if 'h' in self.gates:
            inact = np.zeros((self.numtests,self.numpoints))
            h_tau =  np.zeros((self.numtests,self.numpoints))
            h_inf = np.zeros(self.numtests)
            alpha_h = np.zeros(self.numtests)
            beta_h = np.zeros(self.numtests)
            tau_h = np.zeros(self.numtests)
            alpha_h_hold = self.alphaBetaFit(self.v_hold, self.v_half_h_a, self.k_h_a, self.rate_h_a, self.a_h_a,self.b_h_a,self.c_h_a,self.d_h_a)
            beta_h_hold = self.alphaBetaFit(self.v_hold, self.v_half_h_b, self.k_h_b, self.rate_h_b, self.a_h_b,self.b_h_b,self.c_h_b,self.d_h_b)
            if (alpha_h_hold + beta_h_hold) != 0:
                h_inf_hold = alpha_h_hold / (alpha_h_hold + beta_h_hold)
            else:
                h_inf_hold = 0
            h = h_inf_hold

        Vstim = self.protocol_end
        for i in range(0,self.numtests):
            V_ss[i] = Vstim
            for j in range(self.onset-1,self.offset):
                V[i][j] = Vstim
            Vstim -= self.protocol_steps

        if self.pc_type == 'IClamp':
            for i in range(0,self.numtests):
                for j in range(0,self.numpoints):
                    if hasattr(self,'gL'):
                        I_in[i][j] = -self.gL*(self.v_hold - self.VL)
                    else:
                        I_in[i][j] = self.I_init

            Istim = -self.protocol_start
            for i in range(0,self.numtests):
                for j in range(self.onset-1,self.offset):
                    I_in[i][j] += Istim
                Istim -= self.protocol_steps

        # Variable initialization
        for j in range(0,self.numtests):
            if 'vda' in self.gates:
                m_inf[j] = self.boltzmannFit(V_ss[j], self.v_half_a, self.k_a, self.rate_a, self.C_a)
                if 'mtau' in self.gates:
                    T_a[j] = self.boltzmannFit(V_ss[j], self.v_half_mt, self.k_mt, self.rate_mt, self.C_mt)**self.mt_power
                else:
                    T_a[j] = self.T_a
            if 'vdi' in self.gates:
                h_inf[j] = self.boltzmannFit(V_ss[j], self.v_half_i, self.k_i, self.rate_i, self.C_i)
                if 'htau' in self.gates:
                    T_i[j] = self.boltzmannFit(V_ss[j], self.v_half_ht, self.k_ht, self.rate_ht, self.C_ht)**self.ht_power
                else:
                    T_i[j] = self.T_i
            if 'm' in self.gates:
                alpha_m[j] = self.alphaBetaFit(V_ss[j], self.v_half_m_a, self.k_m_a, self.rate_m_a, self.a_m_a,self.b_m_a,self.c_m_a,self.d_m_a)
                beta_m[j] = self.alphaBetaFit(V_ss[j], self.v_half_m_b, self.k_m_b, self.rate_m_b, self.a_m_b,self.b_m_b,self.c_m_b,self.d_m_b)
                if (alpha_m[j] + beta_m[j]) != 0:
                    tau_m[j] = 1 / (alpha_m[j] + beta_m[j])
                    m_inf[j] = alpha_m[j] / (alpha_m[j] + beta_m[j])
                else:
                    tau_m[j] = 1e-10
                    m_inf[j] = 0
            if 'h' in self.gates:
                alpha_h[j] = self.alphaBetaFit(V_ss[j], self.v_half_h_a, self.k_h_a, self.rate_h_a, self.a_h_a,self.b_h_a,self.c_h_a,self.d_h_a)
                beta_h[j] = self.alphaBetaFit(V_ss[j], self.v_half_h_b, self.k_h_b, self.rate_h_b, self.a_h_b,self.b_h_b,self.c_h_b,self.d_h_b)
                if (alpha_h[j] + beta_h[j]) != 0:
                    tau_h[j] = 1 / (alpha_h[j] + beta_h[j])
                    h_inf[j] = alpha_h[j] / (alpha_h[j] + beta_h[j])
                else:
                    tau_h[j] = 1e-10
                    h_inf[j] = 0

        for j in range(0,self.numtests):
            for i in range(1,self.numpoints):
                dt = i*self.deltat
                I = self.g * (V[j][i-1] - self.e_rev)
                po = 1

                if 'vda' in self.gates:
                    if self.onset < i < self.offset:
                        if 'n_t' in self.sim_params:
                            m = m_inf[j] - ((m_inf[j] - m_inf_hold) * exp(-dt / T_a[j]))                            
                        else:
                            da = (m_inf[j] - m)/T_a[j]
                            m += (da*self.deltat)
                    else:
                        if 'n_t' in self.sim_params:
                            m = m_inf_hold
                        else:
                            da = (m_inf_hold - m)/T_a[j]
                            m += (da*self.deltat)

                    # Preventing overflow when fitting parameters are inappropriate
                    # if m > 1:
                    #     m = 1
                    # elif m < 0:
                    #     m = 0

                    act[j][i] = m**self.a_power
                    po *= act[j][i]

                if 'vdi' in self.gates:
                    if self.onset < i < self.offset:
                        if 'n_t' in self.sim_params:
                            h = h_inf[j] - ((h_inf[j] - h_inf_hold) * exp(-dt / T_i[j]))
                        else:
                            di = (h_inf[j] - h)/T_i[j]
                            h += (di*self.deltat)
                    else:
                        if 'n_t' in self.sim_params:
                            h = h_inf_hold
                        else:
                            di = (h_inf_hold - h)/T_i[j]
                            h += (di*self.deltat)

                    # Preventing overflow when parameters are inappropriate
                    if h > 1:
                        h = 1
                    elif h < 0:
                        h = 0

                    inact[j][i] = h**self.i_power
                    po *= inact[j][i]

                if 'cd' in self.gates:
                    cd_inf[j][i] = self.boltzmannFit(Ca[j][i-1], self.ca_half, self.k_ca)
                    cd[j][i] = (1 + (cd_inf[j][i] - 1) * self.alpha_ca)**self.cd_power
                    po *= cd[j][i]

                    dCa = -(Ca[j][i-1] / self.T_ca + self.thi_ca * I * po)
                    Ca[j][i] = Ca[j][i-1] + dCa * self.deltat

                if 'm' in self.gates:
                    if self.onset < i < self.offset:
                        dm = (alpha_m[j]*(1.0-m)) - (beta_m[j]*m)
                        m_tau[j][i] = (m_inf[j] - ((m_inf[j] - m_inf_hold)*np.exp(-dt/tau_m[j])))**self.m_power
                    else:
                        dm = (alpha_m_hold*(1.0-m)) - (beta_m_hold*m)
                        m_tau[j][i] = m_inf_hold**self.m_power
                    m += (dm*self.deltat)

                    # Preventing overflow when fitting parameters are inappropriate
                    if m > 1:
                        m = 1
                    elif m < 0:
                        m = 0
                    act[j][i] = m**self.m_power
                    po *= act[j][i]

                if 'h' in self.gates:
                    if self.onset < i < self.offset:
                        dh = (alpha_h[j]*(1.0-h)) - (beta_m[j]*h)
                        h_tau[j][i] = h_inf[j] - ((h_inf[j] - h_inf_hold)*np.exp(-dt/tau_h[j]))**self.h_power
                    else:
                        dh = (alpha_h_hold*(1.0-h)) - (beta_h_hold*h)
                        h_tau[j][i] = h_inf_hold**self.h_power
                    h += (dh*self.deltat)

                    # Preventing overflow when parameters are inappropriate
                    if h > 1:
                        h = 1
                    elif h < 0:
                        h = 0
                    inact[j][i] = h**self.h_power
                    po *= inact[j][i]

                PO[j][i] = po
                I_mem[j][i] = I * po

                if hasattr(self,'gL'):
                    IL = self.gL*(V[j][i-1] - self.VL)
                    I_mem[j][i] += IL

                if self.pc_type == 'IClamp':
                    # dv = -(I_in[j][i] + I_mem[j][i]) / self.c_mem
                    if hasattr(self,'gL'):
                        dv = -(I_in[j][i] + I_mem[j][i] + IL)
                    else:
                        dv = -(I_in[j][i] + I_mem[j][i])
                    V[j][i] = V[j][i-1] + dv * self.deltat

                if self.onset < i < self.offset:
                    if abs(I_mem[j][i]) > abs(I_max[j]):
                        I_max[j] = I_mem[j][i]
                        V_max[j] = V_ss[j]
                    if po > PO_max[j]:
                        PO_max[j] = po
                        V_PO_max[j] = V_ss[j]
                    if self.pc_type == 'IClamp':
                        if abs(V_max[j][i]) > abs(V_max[j]):
                            V_max[j] = V[j][i]
                        if abs(V_PO_max[j][i]) > abs(V_PO_max[j]):
                            V_PO_max[j] = V[j][i]

            I_mem[j][0] = I_mem[j][1]
            I_ss[j] = I_mem[j][self.offset-1]

        self.results['t'] = self.xaxis
        self.results['V'] = V
        self.results['I'] = I_mem
        self.results['PO'] = PO
        self.results['V_ss'] = V_ss
        self.results['V_max'] = V_max
        self.results['V_PO_max'] = V_PO_max
        if self.act_fit:
            self.results['I_ss'] = self.iv_act(V_ss)
            self.results['I_max'] = self.results['I_ss']
            self.results['PO_ss'] = self.pov_act(V_ss)
            self.results['PO_max'] = self.results['PO_ss']
        else:
            self.results['I_max'] = I_max
            self.results['I_ss'] = I_ss
            self.results['PO_max'] = PO_max
            self.results['PO_ss'] = PO[:, self.offset-1]
        if self.pov_fit:
            self.results['PO_ss'] = self.pov(V_ss)
        if 'vda' in self.gates:
            self.results['act'] = act
            self.results['m_inf'] = m_inf
        if 'vdi' in self.gates:
            self.results['inact'] = inact
            self.results['h_inf'] = h_inf
        if 'cd' in self.gates:
            self.results['Ca'] = Ca
            self.results['cd'] = cd
            self.results['cd_inf'] = cd_inf[:, self.offset-1]
        if 'm' in self.gates:
            self.results['m_inf'] = m_inf
            self.results['alpha_m'] = alpha_m
            self.results['beta_m'] = beta_m
            self.results['m_tau'] = m_tau[:, self.offset-1]
            self.results['tau_m'] = tau_m
            # self.results['PO'] = m_tau
            # self.results['PO_ss'] = m_tau[:, self.offset-1]
        if 'h' in self.gates:
            self.results['h_inf'] = h_inf
            self.results['alpha_h'] = alpha_h
            self.results['beta_h'] = beta_h
            self.results['h_tau'] = h_tau[:, self.offset-1]
            self.results['tau_h'] = tau_h
        if 'mtau' in self.gates:
            self.results['m_tau'] = T_a
        if 'htau' in self.gates:
            self.results['h_tau'] = T_i

        if len(t) > 0 and not hasattr(self,'trace_size'):
            if self.pc_type == 'IClamp':
                index = [np.abs(np.asarray(self.xaxis) - target_x).argmin() for target_x in t]
                V_t = [V[0][i] for i in index]
                return V_t
            else:
                index = [np.abs(np.asarray(self.xaxis) - np.asarray(target_x)).argmin() for target_x in t]
                I_t = [I_mem[0][i] for i in index]
                return I_t
        else:
            return self.results

    def iv_act(self,V,*args):

        if len(args)>0:
            self.zparams = dict(zip(self.fit_params,args))
        else:
            self.zparams = self.channel_params

        if 'g_cap' in self.zparams:
            g = self.zparams['g_cap'] * self.c_mem
        elif ('g_dens' in self.zparams):
            g = self.zparams['g_dens'] * self.c_mem / self.cell_params['spec_cap']
        else:
            g = self.zparams['g']

        if 'gL' in self.zparams:
            if 'g_cap' in self.zparams:
                self.gL *= self.c_mem
            elif ('g_dens' in self.zparams):
                self.gL *= (self.c_mem / self.cell_params['spec_cap'])
            else:
                self.gL = self.zparams['gL']
            self.VL = self.zparams['VL']

        I_act = g * (1/(1 + np.exp((self.zparams['v_half_a'] - V)/self.zparams['k_a'])))**self.a_power * (V - self.zparams['e_rev'])
        if 'gL' in self.zparams:
            I_act += self.gL*(V - self.VL)

        return I_act

    def pov_act(self,V,*args):

        if len(args)>0:
            self.zparams = dict(zip(self.fit_params,args))
        else:
            self.zparams = self.channel_params

        PO_act = (1/(1 + np.exp((self.zparams['v_half_a'] - V)/self.zparams['k_a'])))**self.a_power

        return PO_act

    def pov(self,V,*args):

        if len(args)>0:
            self.zparams = dict(zip(self.fit_params,args))
        else:
            self.zparams = self.channel_params

        PO = (1/(1 + np.exp((self.zparams['v_half_a'] - V)/self.zparams['k_a'])))**self.a_power

        if 'vdi' in self.gates:
            PO_vdi = (1/(1 + np.exp((self.zparams['v_half_i'] - V)/self.zparams['k_i'])))**self.i_power
            PO = np.multiply(PO,PO_vdi)

        # if 'cd' in self.gates:
        #     cd_inf = (1/(1 + np.exp((self.zparams['ca_half'] - (PO*self.ca_con))/self.zparams['k_ca'])))
        #     PO_cd = (1+((cd_inf-1)*self.zparams['alpha_ca']))**self.cd_power
        #     PO = np.multiply(PO,PO_cd)

        return PO

    def n_tau_fit(self,t,*args):

        if len(args)>0:
            self.zparams = dict(zip(self.fit_params,args))
        else:
            self.zparams = self.channel_params

        if 'm' in self.gates and 'a_m_a' in self.gates['m']:
            self.zparams.update(dict(zip(self.gates['m'].keys(),self.gates['m'].values())))
        if 'h' in self.gates and 'a_h_a' in self.gates['h']:
            self.zparams.update(dict(zip(self.gates['h'].keys(),self.gates['h'].values())))

        if 'V' in self.zparams:
            V = self.zparams['V']
        else:
            V = self.protocol_start

        if 'g_cap' in self.zparams:
            g = self.zparams['g_cap'] * self.c_mem
        elif ('g_dens' in self.zparams):
            g = self.zparams['g_dens'] * self.c_mem / self.cell_params['spec_cap']
        else:
            g = self.zparams['g']

        if 'gL' in self.zparams:
            if 'g_cap' in self.zparams:
                self.gL *= self.c_mem
            elif ('g_dens' in self.zparams):
                self.gL *= (self.c_mem / self.cell_params['spec_cap'])
            else:
                self.gL = self.zparams['gL']
            self.VL = self.zparams['VL']

        if 'm' in self.gates:
            alpha_m_hold = self.alphaBetaFit(self.v_hold, self.zparams['v_half_m_a'], self.zparams['k_m_a'], self.zparams['rate_m_a'], self.zparams['a_m_a'],self.zparams['b_m_a'],self.zparams['c_m_a'],self.zparams['d_m_a'])
            beta_m_hold = self.alphaBetaFit(self.v_hold, self.zparams['v_half_m_b'], self.zparams['k_m_b'], self.zparams['rate_m_b'], self.zparams['a_m_b'],self.zparams['b_m_b'],self.zparams['c_m_b'],self.zparams['d_m_b'])

            n0 = np.divide(alpha_m_hold, (alpha_m_hold + beta_m_hold))

            alpha = self.alphaBetaFit(V, self.zparams['v_half_m_a'], self.zparams['k_m_a'], self.zparams['rate_m_a'], self.zparams['a_m_a'],self.zparams['b_m_a'],self.zparams['c_m_a'],self.zparams['d_m_a'])
            beta = self.alphaBetaFit(V, self.zparams['v_half_m_b'], self.zparams['k_m_b'], self.zparams['rate_m_b'], self.zparams['a_m_b'],self.zparams['b_m_b'],self.zparams['c_m_b'],self.zparams['d_m_b'])

            tau = np.divide(1, (alpha + beta))
            nv = np.divide(alpha, (alpha + beta))

            n = nv - ((nv - n0)*np.exp(-t/tau))
            I = g * n**self.m_power * (V - self.zparams['e_rev'])

        if 'mtau' in self.gates:
            tau = self.boltzmannFit(V, self.zparams['v_half_mt'], self.zparams['k_mt'], self.zparams['rate_mt'])**self.mt_power
            n0 = self.boltzmannFit(self.v_hold, self.zparams['v_half_a'], self.zparams['k_a'])
            nv = self.boltzmannFit(V, self.zparams['v_half_a'], self.zparams['k_a'])

            n = nv - ((nv - n0)*np.exp(-t/tau))
            I = g * n**self.a_power * (V - self.zparams['e_rev'])

        if 'h' in self.gates:
            alpha_h_hold = self.alphaBetaFit(self.v_hold, self.zparams['v_half_h_a'], self.zparams['k_h_a'], self.zparams['rate_h_a'], self.zparams['a_h_a'],self.zparams['b_h_a'],self.zparams['c_h_a'],self.zparams['d_h_a'])
            beta_h_hold = self.alphaBetaFit(self.v_hold, self.zparams['v_half_h_b'], self.zparams['k_h_b'], self.zparams['rate_h_b'], self.zparams['a_h_b'],self.zparams['b_h_b'],self.zparams['c_h_b'],self.zparams['d_h_b'])

            n0 = np.divide(alpha_h_hold, (alpha_h_hold + beta_h_hold))

            alpha = self.alphaBetaFit(V, self.zparams['v_half_h_a'], self.zparams['k_h_a'], self.zparams['rate_h_a'], self.zparams['a_h_a'],self.zparams['b_h_a'],self.zparams['c_h_a'],self.zparams['d_h_a'])
            beta = self.alphaBetaFit(V, self.zparams['v_half_h_b'], self.zparams['k_h_b'], self.zparams['rate_h_b'], self.zparams['a_h_b'],self.zparams['b_h_b'],self.zparams['c_h_b'],self.zparams['d_h_b'])

            tau = np.divide(1, (alpha + beta))
            nv = np.divide(alpha, (alpha + beta))

            n_h = nv - ((nv - n0)*np.exp(-t/tau))
            I *= n_h**self.h_power

        if 'htau' in self.gates:
            tau = self.boltzmannFit(V, self.zparams['v_half_ht'], self.zparams['k_ht'], self.zparams['rate_ht'])**self.ht_power
            n0 = self.boltzmannFit(self.v_hold, self.zparams['v_half_i'], self.zparams['k_i'])
            nv = self.boltzmannFit(V, self.zparams['v_half_i'], self.zparams['k_i'])

            n_h = nv - ((nv - n0)*np.exp(-t/tau))
            I *= n_h**self.i_power

        # if 'cd' in self.gates:
        #     cd_inf = (1/(1 + np.exp((self.zparams['ca_half'] - V)/self.zparams['k_ca'])))
        #     PO_cd = (1+((cd_inf-1)*self.zparams['alpha_ca']))**self.cd_power
        #     PO = np.multiply(PO,PO_cd)

        if 'gL' in self.zparams:
            I += self.gL*(V - self.VL)

        return I

    def n_inf(self,V,*args):

        if len(args)>0:
            self.zparams = dict(zip(self.fit_params,args))
        else:
            self.zparams = self.channel_params

        if 'm' in self.gates and 'a_m_a' in self.gates['m']:
            self.zparams.update(dict(zip(self.gates['m'].keys(),self.gates['m'].values())))
        if 'h' in self.gates and 'a_h_a' in self.gates['h']:
            self.zparams.update(dict(zip(self.gates['h'].keys(),self.gates['h'].values())))

        alpha = self.alphaBetaFit(V, self.zparams['v_half_m_a'], self.zparams['k_m_a'], self.zparams['rate_m_a'], self.zparams['a_m_a'],self.zparams['b_m_a'],self.zparams['c_m_a'],self.zparams['d_m_a'])
        beta = self.alphaBetaFit(V, self.zparams['v_half_m_b'], self.zparams['k_m_b'], self.zparams['rate_m_b'], self.zparams['a_m_b'],self.zparams['b_m_b'],self.zparams['c_m_b'],self.zparams['d_m_b'])

        ninf = (np.divide(alpha, (alpha + beta))**self.m_power)

        if 'h' in self.gates:

            alpha = self.alphaBetaFit(V, self.zparams['v_half_h_a'], self.zparams['k_h_a'], self.zparams['rate_h_a'], self.zparams['a_h_a'],self.zparams['b_h_a'],self.zparams['c_h_a'],self.zparams['d_h_a'])
            beta = self.alphaBetaFit(V, self.zparams['v_half_h_b'], self.zparams['k_h_b'], self.zparams['rate_h_b'], self.zparams['a_h_b'],self.zparams['b_h_b'],self.zparams['c_h_b'],self.zparams['d_h_b'])
            ninf *= (np.divide(alpha, (alpha + beta))**self.h_power)

        return ninf

    def tau_n(self,V,*args):

        if len(args)>0:
            self.zparams = dict(zip(self.fit_params,args))
        else:
            self.zparams = self.channel_params

        alpha = self.alphaBetaFit(V, self.v_half_m_a, self.k_m_a, self.rate_m_a, self.a_m_a,self.b_m_a,self.c_m_a,self.d_m_a)
        beta = self.alphaBetaFit(V, self.v_half_m_b, self.k_m_b, self.rate_m_b, self.a_m_b,self.b_m_b,self.c_m_b,self.d_m_b)

        tau = np.divide(1, (alpha + beta))

        return tau

    def optim_curve(self, params, best_candidate, target, curve_type='IV'):
        """
        Returns optimum parameters using a first guess by Scipy Curve_fit

        :param params: parameters to be optimized
        :param best_candidate: First guess for parameter values
        :param target: Digitized data for specified curve
        :param curve_type: Curve type for calling specific function
        :return: Optimized values and related dictionary
        """

        self.target = target
        X = np.asarray(target[0])
        Y = np.asarray(target[1])
        popt = []

        # in scipy leastsq, number of parameters must not exceed number of points.
        diff = len(best_candidate) - len(X)
        if diff > 0:
            for i in range(0,diff):
                X = np.append(X,X[-1])
                Y = np.append(Y,Y[-1])

        self.fit_params = params
        if curve_type == 'IV':
            popt,pcov = curve_fit(self.iv_act, X,Y,best_candidate)
        elif curve_type == 'POV_act':
            popt,pcov = curve_fit(self.pov_act, X,Y,best_candidate)
        elif curve_type == 'POV':
            popt,pcov = curve_fit(self.pov, X,Y,best_candidate)
        elif curve_type == 'VClamp':
            popt,pcov = curve_fit(self.patch_clamp, X,Y,best_candidate)
        elif curve_type == 'n_tau_fit':
            popt,pcov = curve_fit(self.n_tau_fit, X,Y,best_candidate)
        elif curve_type == 'tau_n':
            popt,pcov = curve_fit(self.tau_n, X,Y,best_candidate)
        elif curve_type == 'n_inf':
            popt,pcov = curve_fit(self.n_inf, X,Y,best_candidate)

        return popt, self.zparams

    def vclamp_leastsq(self, params, best_candidate, sampleData, args):

        self.fit_params = params
        self.trace_size = [0]
        X_f = []
        Y_f = []
        on = self.sim_params['start_time']
        off = self.sim_params['end_time']
        if 'weight' in args:
            weight = args['weight']
        else:
            weight = {}
        if 'ftol' in args:
            ftol = args['ftol']
        else:
            ftol = 1.49012e-08
        if 'xtol' in args:
            xtol = args['xtol']
        else:
            xtol = 1.49012e-08
        if 'full_output' in args:
            full_output = args['full_output']
        else:
            full_output = 0

        def ErrorFunc(p,*args):
            x = args[0]
            y = args[1]

            pc_res = self.patch_clamp(x,p)
            Y_res = []
            for i in range(0,len(self.trace_size)-1):
                # Check if POV data is also available
                if i == len(self.trace_size)-2 and hasattr(self,'POV_least'):
                    if 'POV' in weight:
                        weight_pov = weight['POV']
                    else:
                        weight_pov = 1
                    index = [np.abs(np.asarray(pc_res['V_ss']) - np.asarray(target_x)).argmin() for target_x in x[self.trace_size[i]:self.trace_size[i+1]]]
                    if 'PO_peak' in self.POV_least:
                        # pc_res['PO_max'][index][pc_res['PO_max'][index] == 0] = 1e-100
                        I_norm = np.divide(pc_res['I_max'][index],pc_res['PO_max'][index])
                        I_norm[np.isnan(I_norm)] = 0
                        Y_res.extend([pc_res['I_max'][j]*weight_pov for j in index])
                        y[self.trace_size[i]:self.trace_size[i+1]] = np.multiply(y[self.trace_size[i]:self.trace_size[i+1]],I_norm)*weight_pov
                    else:
                        # pc_res['PO_ss'][index][pc_res['PO_ss'][index] == 0] = 1e-100
                        I_norm = np.divide(pc_res['I_ss'][index],pc_res['PO_ss'][index])
                        I_norm[np.isnan(I_norm)] = 0
                        Y_res.extend([pc_res['I_ss'][j]*weight_pov for j in index])
                        y[self.trace_size[i]:self.trace_size[i+1]] = np.multiply(y[self.trace_size[i]:self.trace_size[i+1]],I_norm)*weight_pov
                else:
                    index = [np.abs(np.asarray(self.xaxis) - np.asarray(target_x)).argmin() for target_x in x[self.trace_size[i]:self.trace_size[i+1]]]
                    Y_res.extend([pc_res['I'][i][j] for j in index])

            cost = np.asarray(y)-np.asarray(Y_res)

            return cost

        for i,trace in enumerate(sampleData['VClamp']['traces']):
            X = np.asarray(trace['t'])
            Y = np.asarray(trace['I'])
            X_f.extend(X)
            Y_f.extend(Y)
            self.trace_size.append(self.trace_size[i]+len(X))

        if 'POV' in sampleData:
            X_f.extend(sampleData['POV']['V'])
            if 'PO_peak' in sampleData['POV']:
                self.POV_least = 'PO_peak'
                Y_f.extend(sampleData['POV']['PO_peak'])
            else:
                self.POV_least = 'PO'
                Y_f.extend(sampleData['POV']['PO'])
            self.trace_size.append(self.trace_size[-1]+len(sampleData['POV']['V']))

        result, cov = leastsq(ErrorFunc, best_candidate, args=(X_f,Y_f), full_output=full_output,ftol=ftol, xtol=xtol)

        return result
