"""
ChannelWorm fitter module for generating models and plots after optimization.
"""

import matplotlib.pyplot as plt

class Modelator(object):

    def __init__(self, bio_params, sim_params):

        self.cell_params = bio_params['cell_params']
        self.channel_params = bio_params['channel_params']
        self.sim_params = sim_params

    def compare_plots(self,sampleData,simData,show=False):
        """
        Generates originals vs simulated plots
        """

        # TODO: Add path and GUID to save plots
        
        if 'VClamp' in sampleData:

            ref = sampleData['VClamp']['ref']
            for trace in sampleData['VClamp']['traces']:
                if 'vol' in trace and trace['vol']:
                    # sample_plot, = plt.plot(trace['t'],trace['I'], label = '%i (V)'%trace['vol'])
                    sample_plot, = plt.plot(trace['t'],trace['I'], 'ko')
                else:
                    # sample_plot, = plt.plot(trace['t'],trace['I'], marker = '.', linestyle='', color='k')
                    sample_plot, = plt.plot(trace['t'],trace['I'], 'ko')

            voltage = self.sim_params['protocol_end']
            for trace in simData['I']:
                # model_plot, = plt.plot(simData['t'],trace, label = '%i (V)'%voltage)
                model_plot, = plt.plot(simData['t'],trace, color='r')
                voltage -= self.sim_params['protocol_steps']
            plt.legend([sample_plot,model_plot], ["Original data from Fig.%s, DOI: %s"%(ref['fig'],ref['doi']),"Best model"])
            plt.title("The Best Model fitted to data for voltage-clamp using GA")
            plt.xlabel("Time (s)")
            plt.ylabel("Current (A)")
            plt.savefig("data_vs_candidate-VClamp.png",bbox_inches='tight',format='png')

            if show:
                plt.show()

        if 'IClamp' in sampleData:

            ref = sampleData['IClamp']['ref']
            for trace in sampleData['IClamp']['traces']:
                if 'amp' in trace and trace['amp']:
                    # sample_plot, = plt.plot(trace['t'],trace['V'], label = '%i (A)'%trace['amp'])
                    sample_plot, = plt.plot(trace['t'],trace['V'], 'ko')
                else:
                    # sample_plot, = plt.plot(trace['t'],trace['V'], marker = '.', linestyle='', color='k')
                    sample_plot, = plt.plot(trace['t'],trace['V'], 'ko')

            amp = self.sim_params['protocol_end']
            for trace in simData['V']:
                # model_plot, = plt.plot(simData['t'],trace, label = '%i (A)'%amp)
                model_plot, = plt.plot(simData['t'],trace, color='r')
                amp -= self.sim_params['protocol_steps']

            plt.legend([sample_plot,model_plot], ["Original data from Fig.%s, DOI: %s"%(ref['fig'],ref['doi']),"Best model"])
            plt.title("The Best Model fitted to data for current-clamp using GA")
            plt.xlabel("Time (s)")
            plt.ylabel("Voltage (V)")
            plt.savefig("data_vs_candidate-IClamp.png",bbox_inches='tight',format='png')

            if show:
                plt.show()

        if 'IV' in sampleData:

            ref = sampleData['IV']['ref']
            if 'I_peak' in sampleData['IV']:
                sample_plot, = plt.plot([round(x*1e3) for x in sampleData['IV']['V']],sampleData['IV']['I_peak'],'ko')
                model_plot, = plt.plot([round(x*1e3) for x in simData['V_max']],simData['I_max'],'r')
            else:
                sample_plot, = plt.plot([round(x*1e3) for x in sampleData['IV']['V']],sampleData['IV']['I'],'ko')
                model_plot, = plt.plot([round(x*1e3) for x in simData['V_ss']],simData['I_ss'],'r')
            plt.legend([sample_plot,model_plot], ["Original data from Fig.%s, DOI: %s"%(ref['fig'],ref['doi']),"Best model"])
            plt.title("The Best Model fitted to data for I/V curve using GA")
            plt.xlabel("Voltage (mV)")
            plt.ylabel("Current (A/F)")
            plt.savefig("data_vs_candidate-IV.png",bbox_inches='tight',format='png')

            if show:
                plt.show()

        if 'POV' in sampleData:

            ref = sampleData['POV']['ref']
            if 'PO_peak' in sampleData['POV']:
                sample_plot, = plt.plot([round(x*1e3) for x in sampleData['POV']['V']],sampleData['POV']['PO_peak'],'ko')
                model_plot, = plt.plot([round(x*1e3) for x in simData['V_PO_max']],simData['PO_max'],'r')
            else:
                sample_plot, = plt.plot([round(x*1e3) for x in sampleData['POV']['V']],sampleData['POV']['PO'],'ko')
                model_plot, = plt.plot([round(x*1e3) for x in simData['V_ss']],simData['PO_ss'],'r')
            plt.legend([sample_plot,model_plot], ["Original data from Fig.%s, DOI: %s"%(ref['fig'],ref['doi']),"Best model"])
            plt.title("The Best Model fitted to data for G/Gmax / V curve using GA")
            plt.xlabel("Voltage (mV)")
            plt.ylabel("G/Gmax")
            plt.savefig("data_vs_candidate-POV.png",bbox_inches='tight',format='png')

            if show:
                plt.show()

    def generate_nml2(self):
        """

        :return:
        """

    def run_nml2(self):
        """

        :return:
        """
