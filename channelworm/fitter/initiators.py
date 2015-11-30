"""
ChannelWorm fitter module for initializing needed parameters.
"""
import matplotlib.pyplot as plt
import channelworm

class Initiator(object):

    def __init__(self, userData={}):

        """Initializes variables for other modules

        :param user: parameters related to user profile
        """

        # TODO: Initialize data provided by user (directly from interface or from DB)

        if 'sample' in userData:
            self.sampleData = userData['samples']
        self.sim_params = dict() # userData['sim_params']
        self.opt_params = dict() # userData['opt_params']
        self.bio_params = dict() # userData['bio_params']

    def get_bio_params(self):
        """
        Get parameters for cell and channel from user / DB and initialize variables.

        """

        # TODO: Get values from pyOW

        self.bio_params['cell_type'] = 'ADAL'
        self.bio_params['channel_type'] = 'EGL-19'
        self.bio_params['ion_type'] = 'Ca'
        self.bio_params['I_leak'] = False

        self.bio_params['cell_params'] =      ['C_mem', 'area', 'spec_cap']
        self.bio_params['unit_cell_params'] = ['F',     'm2',   'F/m2']
        self.bio_params['val_cell_params'] =  [7.5e-11, 7.5e-9, 0.01]

        # self.bio_params['cell_channel_params'] = ['channel_density']
        # self.bio_params['unit_cell_channel_params'] = ['1/m2']
        # self.bio_params['val_cell_channel_params'] = []

        # g (S) = (g_dens (S/m2) / spec_cap (F/m2)) * C_mem (F)

        self.bio_params['gate_params'] = {'vda': {'power': 1},'vdi': {'power': 1},'cdi': {'power': 1}}

        self.bio_params['channel_params'] = ['g_dens','e_rev']
        self.bio_params['unit_chan_params'] = ['S/m2','V']

        self.bio_params['min_val_channel'] = [1, -150e-3]
        self.bio_params['max_val_channel'] = [10, 150e-3]

        if self.bio_params['I_leak']:

            self.bio_params['channel_params'].extend(['gL',   'VL'])
            self.bio_params['unit_chan_params'].extend(['S/m2','V'])

            self.bio_params['min_val_channel'].extend([5e-2,-2e-2]) # chr2
            self.bio_params['max_val_channel'].extend([5e-1, 4e-2]) # chr2

        if 'vda' in self.bio_params['gate_params']:

            self.bio_params['channel_params'].extend(['v_half_a','k_a','T_a'])
            self.bio_params['unit_chan_params'].extend(['V','V','s'])

            self.bio_params['min_val_channel'].extend([-0.15, 0.0001, 0.0001])
            self.bio_params['max_val_channel'].extend([ 0.15,   0.1,  0.01])

        if 'vdi' in self.bio_params['gate_params']:

            self.bio_params['channel_params'].extend(['v_half_i','k_i','T_i'])

            self.bio_params['unit_chan_params'].extend(['V','V','s'])

            self.bio_params['min_val_channel'].extend([-150e-3, -0.1,  0.0001])
            self.bio_params['max_val_channel'].extend([ 150e-3, -0.0001, 0.01])

        if 'cdi' in self.bio_params['gate_params']:

            #Parameters for Ca-dependent inactivation (Boyle & Cohen 2008)
            self.bio_params['channel_params'].extend(['ca_half_i','alpha_ca','k_ca','T_ca'])
            self.bio_params['unit_chan_params'].extend(['M','','M','s'])

            self.bio_params['min_val_channel'].extend([1e-9, 0.1, -1e-6, 1e-3])
            self.bio_params['max_val_channel'].extend([1e-6, 0.9, -1e-9, 1])

            # Boyle & Cohen: thiCa = 6.1e-6/(T_Ca*gCa)
            # NeuroML: thiCa = ca_rho / area_m2

        return self.bio_params

    def get_opt_params(self, type='GA'):
        """
        Get parameters for optimization algorithms.

        :param type: Type of algorithm (GA, PSO)
        :return: Dict of parameters
        """

        # TODO: Initialize data provided by user (directly from interface or from DB)

        if type == 'GA':
            self.opt_params['population_size'] = 3
            self.opt_params['max_evaluations'] = 6
            self.opt_params['num_selected'] = 2
            self.opt_params['num_offspring'] = 15
            self.opt_params['num_elites'] = 1
            self.opt_params['mutation_rate'] = 0.05
            self.opt_params['maximize'] = False
            self.opt_params['seeds'] = None
            self.opt_params['verbose'] = True

        if type == 'PSO':
            self.opt_params['swarmsize'] = 100
            self.opt_params['maxiter'] = 100
            self.opt_params['minstep'] = 1e-22
            self.opt_params['minfunc'] = 1e-22
            self.opt_params['debug'] = True
            self.opt_params['I_dist'] = 1e-8
            self.opt_params['V_dist'] = 1e-22
            self.opt_params['IV_dist'] = 1e-22
            self.opt_params['POV_dist'] = 4e-3

        return self.opt_params

    def get_sim_params(self,type='VClamp'):
        """
        Get simulation parameters from user / DB and initialize variables.

        """

        # TODO: Get values from pyOW

        if self.bio_params['channel_type'] == 'EGL-19':

            # for VClamp -- Boyle & Cohen 2008
            self.sim_params['v_init'] = -75e-3
            self.sim_params['deltat'] = 1e-5
            self.sim_params['duration'] = 0.22
            self.sim_params['start_time'] = 0.008
            self.sim_params['end_time'] = 0.208
            self.sim_params['protocol_start'] = -70e-3
            self.sim_params['protocol_end'] = 40e-3
            self.sim_params['protocol_steps'] = 10e-3
            self.sim_params['ion_type'] = 'Ca'

        if 'IV' in type:

            # # for IV -- Boyle & Cohen 2008
            self.sim_params.update({'IV':{}})
            self.sim_params['IV']['v_init'] = -70e-3
            self.sim_params['IV']['deltat'] = 1e-5
            self.sim_params['IV']['duration'] = 0.03
            self.sim_params['IV']['start_time'] = 0.002
            self.sim_params['IV']['end_time'] = 0.022
            self.sim_params['IV']['protocol_start'] = -40e-3
            self.sim_params['IV']['protocol_end'] = 80e-3
            self.sim_params['IV']['protocol_steps'] = 10e-3
            self.sim_params['IV']['ion_type'] = 'Ca'

        if 'IClamp' in type:

            # for IClamp -- Boyle & Cohen 2008
            self.sim_params.update({'IC':{}})
            self.sim_params['IC']['v_hold'] = -75e-3
            self.sim_params['IC']['I_init'] = 0
            self.sim_params['IC']['pc_type'] = 'IClamp'
            self.sim_params['IC']['deltat'] = 1e-5
            self.sim_params['IC']['duration'] = 0.045
            self.sim_params['IC']['start_time'] = 0.003
            self.sim_params['IC']['end_time'] = 0.045
            self.sim_params['IC']['protocol_start'] = 100e-12
            self.sim_params['IC']['protocol_end'] = 400e-12
            self.sim_params['IC']['protocol_steps'] = 100e-12

        return self.sim_params

    def get_sample_params(self):
        """
        Get experimental parameters from user / DB and initialize variables.
        Data structure for sampleData:

            ['VClamp']
                ['ref']
                    ['fig'] e.g. 2A
                    ['doi'] e.g. 10.1371/journal.pcbi.0030169.
                ['traces']
                    ['vol'] e.g. -30 --> ['amp'] in case of IClamp
                    ['csv_path'] e.g. data/user1/vclampM30.csv
                    ['x_var']
                    ['y_var']
                        ['type'] e.g. current
                        ['unit'] e.g. nA
                        ['toSI'] e.g. 1e-9 # multiply by this value to convert to SI
                        ['adjust'] e.g. -0.5 # add to this value to adjust axis
                    ['t']
                    ['I']
                        [] e.g. -50.5,-49.8,...

            ['IClamp']
            ['IV']

        """

        # For loop to extract all csv files from user's profile path
        #  1: csv files: IClamp, VClamp, IV, G/Gmax, mtau, minf, htau, hinf, etc
        #   1.1: info related to figures, and experiment: x,y variables, references (paper DOI, plot ref), experimental conditions (voltage/current clamped, temprature, etc)

        if 'VClamp' in self.sampleData:
            i = 0
            for trace in self.sampleData['VClamp']['traces']:
                self.sampleData['VClamp']['traces'][i]['t'],self.sampleData['VClamp']['traces'][i]['I'] = \
                    self.csv_to_XY(trace['csv_path'], trace['x_var'], trace['y_var'], self.sampleData['VClamp']['ref'])
                i += 1

        if 'IClamp' in self.sampleData:
            i = 0
            for trace in self.sampleData['IClamp']['traces']:
                self.sampleData['IClamp']['traces'][i]['t'],self.sampleData['IClamp']['traces'][i]['V'] = \
                    self.csv_to_XY(trace['csv_path'], trace['x_var'], trace['y_var'], self.sampleData['IClamp']['ref'])
                i += 1

        if 'IV' in self.sampleData:
            self.sampleData['IV']['V'], I = self.csv_to_XY(self.sampleData['IV']['csv_path'],
                                                            self.sampleData['IV']['x_var'],
                                                            self.sampleData['IV']['y_var'],
                                                            self.sampleData['IV']['ref'])

            if self.sampleData['IV']['y_var']['type'] == 'I_peak':
                self.sampleData['IV']['I_peak'] = I
            else:
                self.sampleData['IV']['I'] = I

        if 'POV' in self.sampleData:
            self.sampleData['POV']['V'],PO = self.csv_to_XY(self.sampleData['POV']['csv_path'],
                                                            self.sampleData['POV']['x_var'],
                                                            self.sampleData['POV']['y_var'],
                                                            self.sampleData['POV']['ref'])

            if self.sampleData['POV']['y_var']['type'] == 'PO_peak':
                self.sampleData['POV']['PO_peak'] = PO
            else:
                self.sampleData['POV']['PO'] = PO

        return self.sampleData

    def csv_to_XY(self,path,x_var,y_var,ref,plot=False):
        """Extracts X,Y data from a csv file and convert to array

        Data must be in a csv and in two columns, (e.g. time and
        voltage, and units should be SI (e.g. Volts and Seconds)).
        :param path: Path to csv file e.g data/user1/vt.csv
        :param x_var: Variable type and unit for the first column parameter of csv file
        :param y_var: Variable type and unit for the second column parameter of csv file
        :param ref: Paper reference including figure
        :param plot: If plot = TRUE, then plot raw data

        :return: two lists - X and Y
        """

        import csv

        x=[]
        y=[]

        with open(path) as f:
            reader = csv.reader(f)
            for row in reader:

                x_value = float(row[0])
                y_value = float(row[1])

                if 'adjust' in x_var:
                    x_value += x_var['adjust']
                if 'adjust' in y_var:
                    y_value += y_var['adjust']

                x.append(x_value * x_var['toSI'])
                y.append(y_value * y_var['toSI'])

        if plot:
            plt.plot(x,y)
            plt.title('Raw data from Fig.%s, DOI: %s'%(ref['fig'],ref['doi']))
            plt.xlabel('%s (%s)'%(x_var['type'],x_var['unit']))
            plt.ylabel('%s (%s)'%(y_var['type'],y_var['unit']))
            plt.show()

        return x,y

    def get_data_from_db(self,fig_id,adjust={},plot=False):
        """
        Get experimental parameters from DB and initialize variables.
        Data structure for sampleData:

            ['VClamp']
                ['ref']
                    ['fig'] e.g. 2A
                    ['doi'] e.g. 10.1371/journal.pcbi.0030169.
                ['traces']
                    ['vol'] e.g. -30 --> ['amp'] in case of IClamp
                    ['csv_path'] e.g. data/user1/vclampM30.csv
                    ['x_var']
                    ['y_var']
                        ['type'] e.g. current
                        ['unit'] e.g. nA
                        ['toSI'] e.g. 1e-9 # multiply by this value to convert to SI
                        ['adjust'] e.g. -0.5 # add to this value to adjust axis
                    ['t']
                    ['I']
                        [] e.g. -50.5,-49.8,...

            ['IClamp']
            ['IV']

        :param fig_id: ID of the figure in channelworm (Look at ID column in www.channelworm.com/ion_channel/graph/)
        :param plot: if TRUE, shows the plot
        :return: Dict of parameters
        """

        I_type = ['I','I_ss','I_peak','Current','Steady-state Current','Peak Current']
        T_type = ['T','Time']
        V_type = ['V','Voltage']
        PO_type = ['I_norm', 'Normalized Current', 'G/G_max', 'Po_peak', 'Peak Open Probability', 'Po', 'Open Probability', 'G', 'Conductance']
        x = []
        y = []

        channelworm.django_setup()
        from ion_channel.models import Graph, GraphData

        graph = Graph.objects.get(id=fig_id)
        graph_data = GraphData.objects.filter(graph__id=graph.id)
        doi = graph.experiment.reference.doi

        ref = {'fig':graph.figure_ref_address,'doi':doi}
        x_var = {'type':graph.x_axis_type,'unit':graph.x_axis_unit,'toSI':graph.x_axis_toSI}
        y_var = {'type':graph.y_axis_type,'unit':graph.y_axis_unit,'toSI':graph.y_axis_toSI}
        graph_dic = {'ref':ref,'x_var':x_var,'y_var':y_var, 'traces':[]}

        for obj in graph_data:
            for i,j in obj.asarray():
                if 'x' in adjust:
                    i += adjust['x']
                if 'y' in adjust:
                    j += adjust['y']
                x.append(i * x_var['toSI'])
                y.append(j * y_var['toSI'])

            if graph.x_axis_type in T_type and graph.y_axis_type in I_type:
                graph_dic['traces'].append({'vol':int(obj.series_name)*1e-3,'t':x,'I':y})

            elif  graph.x_axis_type in T_type and graph.y_axis_type in V_type:
                graph_dic['traces'].append({'amp':int(obj.series_name)*1e-6,'t':x,'V':y})

            elif graph.x_axis_type in V_type and graph.y_axis_type in I_type:
                graph_dic['V'] = x
                if graph.y_axis_type == 'I_peak':
                    graph_dic['I_peak'] = y
                else:
                    graph_dic['I'] = y

            elif graph.x_axis_type in V_type and graph.y_axis_type in PO_type:
                graph_dic['V'] = x
                if graph.y_axis_type == 'Po_peak':
                    graph_dic['PO_peak'] = y
                else:
                    graph_dic['PO'] = y

            if plot:
                plt.plot([i/x_var['toSI'] for i in x],[j/y_var['toSI'] for j in y],'ko')
                plt.title('Raw data from Fig.%s, DOI: %s'%(ref['fig'],ref['doi']))
                plt.xlabel('%s (%s)'%(x_var['type'],x_var['unit']))
                plt.ylabel('%s (%s)'%(y_var['type'],y_var['unit']))

        if plot:
            plt.show()

        return graph_dic
