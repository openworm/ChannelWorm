import matplotlib.pyplot as plt

class Initiator(object):

    def __init__(self, userData):

        """Initializes variables for other modules

        :param user: parameters related to user profile
        """

        #TODO: Initialize data provided by user (directly from interface or from DB)

        self.sampleData = userData['samples']
        self.sim_params = dict() #userData['sim_params']
        self.evol_params = dict() # userData['evol_opts']
        self.bio_params = dict() #userData['bio_params']


    def getBioParameters(self):
        """
        Get parameters for cell and channel from user / DB and initialize variables.

        """

        #TODO: Get values from pyOW

        self.bio_params['cell_type'] = 'ADAL'
        self.bio_params['channel_type'] = 'EGL-19'
        self.bio_params['ion_type'] = 'Ca'

        #Standard spec_cap = 0.01 F/m2
        #From Boyle & Cohen 2008

        self.bio_params['cell_params'] = ['C_mem','area','spec_cap']
        self.bio_params['unit_cell_params'] = ['F','m2','F/m2']
        self.bio_params['val_cell_params'] = [7.23653e-11,7.23653e-9,0.01]

        #self.bio_params['cell_channel_params'] = ['channel_density']
        #self.bio_params['unit_cell_channel_params'] = ['1/m2']
        #self.bio_params['val_cell_channel_params'] = []

        # g (S) = (g_dens (S/m2) / spec_cap (F/m2)) * C_mem (F)

        self.bio_params['channel_params'] = ['g',
                                             'e_rev',
                                             'v_half_a',
                                             'v_half_i',
                                             'k_a',
                                             'k_i',
                                             'T_a',
                                             'T_i',
                                             'a_power',
                                             'i_power']

        self.bio_params['unit_chan_params'] = ['S/F',
                                               'V',
                                               'V',
                                               'V',
                                               'V',
                                               'V',
                                               'S',
                                               'S',
                                               ' ',
                                               ' ']

        self.bio_params['min_val_channel'] = [100 , 0.01, -0.01, 0.01, 0.0001,  -0.001, 0.00001, 0.01, 2, 1]
        # self.bio_params['min_val_channel'] = [1   , -0.01, -0.1, -0.1, 0.000001, -0.1, 0.00001, 0.00001, 2, 1]
        self.bio_params['max_val_channel'] = [500 ,  0.1,-0.001,  0.1,  0.001, -0.0001,   0.001,    1, 2, 1]
        # self.bio_params['max_val_channel'] = [1000 , 0.01, -0.1,  0.1,      0.1, -0.00001,   1,       1, 2, 1]

        # self.bio_params['min_val_channel'] = [220, 0.049, -0.0033, 0.025, 0.006, -0.005, 0.00010, 0.150, 2, 1]
        # self.bio_params['max_val_channel'] = [220, 0.049, -0.0033, 0.025, 0.006, -0.005, 0.00010, 0.150, 2, 1]

        if self.bio_params['ion_type'] == 'Ca':
            self.bio_params['cell_params'].extend(['ca_con'])
            self.bio_params['unit_cell_params'].extend(['M'])
            self.bio_params['val_cell_params'].extend([6.1e-6])

            #Parameters for Ca-dependent inactivation (Boyle & Cohen 2008)
            self.bio_params['channel_params'].extend(['ca_half_i','alpha_ca','k_ca','T_ca','cdi_power'])
            self.bio_params['unit_chan_params'].extend(['M',' ','M','S',' '])

            self.bio_params['min_val_channel'].extend([10e-9,  0.1, -10e-9, 0.5e-3,  1])
            self.bio_params['max_val_channel'].extend([300e-9, 0.4, -150e-9, 20e-3,  1])

            # self.bio_params['min_val_channel'].extend([6.41889e-08, 0.282473, -1.00056e-08, 0.0115, 1])
            # self.bio_params['max_val_channel'].extend([6.41889e-08, 0.282473, -1.00056e-08, 0.0115, 1])

            # Boyle & Cohen: thiCa = 6.1e-6/(T_Ca*gCa)
            # NeuroML: thiCa = ca_rho / area_m2

        return self.bio_params


    def getSimParameters(self,type='VClamp'):
        """
        Get simulation parameters from user / DB and initialize variables.

        """

        #TODO: Get values from pyOW

        self.sim_params['v_init'] = -75e-3
        self.sim_params['deltat'] = 1e-5
        self.sim_params['duration'] = 0.3
        self.sim_params['start_time'] = 0.02
        self.sim_params['end_time'] = 0.22
        self.sim_params['protocol_start'] = -40e-3
        self.sim_params['protocol_end'] = 80e-3
        self.sim_params['protocol_steps'] = 10e-3
        self.sim_params['ion_type'] = 'Ca'

        if type == 'IClamp':
            self.sim_params['v_init_I'] = -75e-3
            self.sim_params['deltat_I'] = 1e-5
            self.sim_params['duration_I'] = 0.045
            self.sim_params['start_time_I'] = 0.005
            self.sim_params['end_time_I'] = 0.025
            self.sim_params['protocol_start_I'] = 100e-12
            self.sim_params['protocol_end_I'] = 400e-12
            self.sim_params['protocol_steps_I'] = 100e-12
            self.sim_params['ion_type_I'] = 'Ca'

        return self.sim_params


    def getSampleParameters(self):
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
                        ['toSI'] e.g. e-9
                    ['t']
                    ['I']
                        [] e.g. -50.5,-49.8,...

            ['IClamp']
            ['IV']

        """

        #TODO: Get values from pyOW

        #For loop to extract all csv files from user's profile path
        # 1: csv files: IClamp, VClamp, IV, G/Gmax, mtau, minf, htau, hinf, etc
        #   1.1: info related to figures, and experiment: x,y variables, references (paper DOI, plot ref), experimental conditions (voltage/current clamped, temprature, etc)

        if 'VClamp' in self.sampleData:
            i = 0
            for trace in self.sampleData['VClamp']['traces']:
                self.sampleData['VClamp']['traces'][i]['t'],self.sampleData['VClamp']['traces'][i]['I'] = self.csv_to_XY(trace['csv_path'], trace['x_var'], trace['y_var'], self.sampleData['VClamp']['ref'])
                i += 1

        if 'IClamp' in self.sampleData:
            i = 0
            for trace in self.sampleData['IClamp']['traces']:
                self.sampleData['IClamp']['traces'][i]['t'],self.sampleData['IClamp']['traces'][i]['V'] = self.csv_to_XY(trace['csv_path'], trace['x_var'], trace['y_var'], self.sampleData['IClamp']['ref'])
                i += 1

        if 'IV' in self.sampleData:
            self.sampleData['IV']['V'],self.sampleData['IV']['I'] = self.csv_to_XY(self.sampleData['IV']['csv_path'], self.sampleData['IV']['x_var'], self.sampleData['IV']['y_var'], self.sampleData['IV']['ref'])

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

                x.append(x_value * x_var['toSI'])
                y.append(y_value * y_var['toSI'])


        if plot:
            plt.plot(x,y)
            plt.title('Raw data from Fig.%s, DOI: %s'%(ref['fig'],ref['doi']))
            plt.xlabel('%s (%s)'%(x_var['type'],x_var['unit']))
            plt.ylabel('%s (%s)'%(y_var['type'],y_var['unit']))
            plt.show()

        return x,y




