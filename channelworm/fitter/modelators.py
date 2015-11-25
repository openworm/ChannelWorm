"""
ChannelWorm fitter module for generating models and plots after optimization.
"""

import matplotlib.pyplot as plt
import neuroml
import neuroml.writers as writers
import lems.api as lems
import osb.metadata
import osb.resources
import sys
from pyneuroml.analysis import NML2ChannelAnalysis
from channelworm.fitter import validators

class Modelator(object):

    def __init__(self, bio_params, sim_params):

        self.cell_params = bio_params['cell_params']
        self.channel_params = bio_params['channel_params']
        self.sim_params = sim_params

    def ss_plots(self,simData,show=False):
        """
        Generates steady state plots for ion channel kinetics (m, h, etc)
        """

        if 'm_inf' in simData:
            plt.plot([round(x*1e3) for x in simData['V_ss']],simData['m_inf'], color='b', label='m_inf')

        if 'h_inf' in simData:
            plt.plot([round(x*1e3) for x in simData['V_ss']],simData['h_inf'], color='r', label='h_inf')

        if 'cdi_inf' in simData:
            plt.plot([round(x*1e3) for x in simData['V_ss']],simData['cdi_inf'], color='y', label='Ca-dependent inactivation')

        plt.legend()
        plt.title("Steady state activation and inactivation versus membrane potential")
        plt.xlabel("Voltage (mV)")
        plt.ylabel("Steady state activation/inactivation")
        plt.savefig("steadystate_vs_voltage.png",bbox_inches='tight',format='png')

        if show:
            plt.show()

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
                    sample_plot, = plt.plot(trace['t'],trace['I'], '--ko')
                else:
                    # sample_plot, = plt.plot(trace['t'],trace['I'], marker = '.', linestyle='', color='k')
                    sample_plot, = plt.plot(trace['t'],trace['I'], '--ko')

            voltage = self.sim_params['protocol_end']
            for trace in simData['I']:
                # model_plot, = plt.plot(simData['t'],trace, label = '%i (V)'%voltage)
                model_plot, = plt.plot(simData['t'],trace, color='r')
                voltage -= self.sim_params['protocol_steps']
            plt.legend([sample_plot,model_plot],
                       ["Original data from Fig.%s, DOI: %s"%(ref['fig'],ref['doi']),"Best model"],
                       loc=9, bbox_to_anchor=(0.9, 0.1))
            plt.title("The Best Model fitted to data for voltage-clamp using optimization")
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
                    sample_plot, = plt.plot(trace['t'],trace['V'], '--ko')
                else:
                    # sample_plot, = plt.plot(trace['t'],trace['V'], marker = '.', linestyle='', color='k')
                    sample_plot, = plt.plot(trace['t'],trace['V'], '--ko')

            amp = self.sim_params['protocol_end']
            for trace in simData['V']:
                # model_plot, = plt.plot(simData['t'],trace, label = '%i (A)'%amp)
                model_plot, = plt.plot(simData['t'],trace, color='r')
                amp -= self.sim_params['protocol_steps']

            plt.legend([sample_plot,model_plot], ["Original data from Fig.%s, DOI: %s"%(ref['fig'],ref['doi']),"Best model"])
            plt.title("The Best Model fitted to data for current-clamp using optimization")
            plt.xlabel("Time (s)")
            plt.ylabel("Voltage (V)")
            plt.savefig("data_vs_candidate-IClamp.png",bbox_inches='tight',format='png')

            if show:
                plt.show()

        if 'IV' in sampleData:

            ref = sampleData['IV']['ref']
            if 'I_peak' in sampleData['IV']:
                sample_plot, = plt.plot([round(x*1e3) for x in sampleData['IV']['V']],sampleData['IV']['I_peak'],'--ko')
                model_plot, = plt.plot([round(x*1e3) for x in simData['V_max']],simData['I_max'],'r')
            else:
                sample_plot, = plt.plot([round(x*1e3) for x in sampleData['IV']['V']],sampleData['IV']['I'],'--ko')
                model_plot, = plt.plot([round(x*1e3) for x in simData['V_ss']],simData['I_ss'],'r')
            plt.legend([sample_plot,model_plot], ["Original data from Fig.%s, DOI: %s"%(ref['fig'],ref['doi']),"Best model"])
            plt.title("The Best Model fitted to data for I/V curve using optimization")
            plt.xlabel("Voltage (mV)")
            plt.ylabel("Current (A/F)")
            plt.savefig("data_vs_candidate-IV.png",bbox_inches='tight',format='png')

            if show:
                plt.show()

        if 'POV' in sampleData:

            ref = sampleData['POV']['ref']
            if 'PO_peak' in sampleData['POV']:
                sample_plot, = plt.plot([round(x*1e3) for x in sampleData['POV']['V']],sampleData['POV']['PO_peak'],'--ko')
                model_plot, = plt.plot([round(x*1e3) for x in simData['V_PO_max']],simData['PO_max'],'r')
            else:
                sample_plot, = plt.plot([round(x*1e3) for x in sampleData['POV']['V']],sampleData['POV']['PO'],'--ko')
                model_plot, = plt.plot([round(x*1e3) for x in simData['V_ss']],simData['PO_ss'],'r')
            plt.legend([sample_plot,model_plot], ["Original data from Fig.%s, DOI: %s"%(ref['fig'],ref['doi']),"Best model"])
            plt.title("The Best Model fitted to data for G/Gmax / V curve using optimization")
            plt.xlabel("Voltage (mV)")
            plt.ylabel("G/Gmax")
            plt.savefig("data_vs_candidate-POV.png",bbox_inches='tight',format='png')

            if show:
                plt.show()

    def generate_channel_nml2(self,bio_params,channel_params,model_params):
        """
        Generates NeuroML2 file from ion channel parameters.

        :param bio_params: Biological parameters
        :param channel_params: Channel parameters
        :param model_params: NeuroML2 file parameters
        :return: NeuroML2 file
        """

        unknowns = ''
        info = 'This is an ion channel model NeuroML2 file generated by ChannelWorm: https://github.com/openworm/ChannelWorm'
        channel_id='ChannelWorm_%s_%s_%s'%(model_params['channel_name'],model_params['channel_id'],model_params['model_id'])

        doc = neuroml.NeuroMLDocument()

        metadata = osb.metadata.RDF(info)

        desc = osb.metadata.Description(channel_id)
        metadata.descriptions.append(desc)

        osb.metadata.add_simple_qualifier(desc,
                                          'bqmodel',
                                          'isDerivedFrom',
                                          "ChannelWorm channel Name: %s channel ID: %s, ModelID: %s"
                                          %(model_params['channel_name'],model_params['channel_id'],model_params['model_id']))

        for reference in model_params['references']:
            DOI = reference['doi']
            pmid = reference['PMID']
            ref_info = reference['citation']
            osb.metadata.add_simple_qualifier(desc,
                                              'bqmodel',
                                              'isDescribedBy',
                                              osb.resources.PUBMED_URL_TEMPLATE % (pmid),
                                              ("DOI: %s, PubMed ID: %s \n"+
                                               "                                 %s") % (DOI, pmid, ref_info))

        species = 'caenorhabditis elegans'

        if osb.resources.KNOWN_SPECIES.has_key(species):
            known_id = osb.resources.KNOWN_SPECIES[species]
            osb.metadata.add_simple_qualifier(desc,
                                              'bqbiol',
                                              'hasTaxon',
                                              osb.resources.NCBI_TAXONOMY_URL_TEMPLATE % known_id,
                                              "Known species: %s; taxonomy id: %s" % (species, known_id))
        else:
            print("Unknown species: %s"%species)
            unknowns += "Unknown species: %s\n"%species

        cell_type = bio_params['cell_type']

        if osb.resources.KNOWN_CELL_TYPES.has_key(cell_type):
            known_id = osb.resources.KNOWN_CELL_TYPES[cell_type]
            osb.metadata.add_simple_qualifier(desc,
                                              'bqbiol',
                                              'isPartOf',
                                              osb.resources.NEUROLEX_URL_TEMPLATE % known_id,
                                              "Known cell type: %s; taxonomy id: %s" % (cell_type, known_id))
        else:
            print("Unknown cell_type: %s"%cell_type)
            unknowns += "Unknown cell_type: %s\n"%cell_type

        # for contributor in model_params['contributors']:
        #     metadata.descriptions.append('Curator: %s (%s)'%(contributor['name'],contributor['email']))

        print("Currently unknown: <<<%s>>>"%unknowns)

        ion = bio_params['ion_type']
        unit = dict(zip(bio_params['channel_params'],bio_params['unit_chan_params']))
        chan = neuroml.IonChannelHH(id=channel_id,
                                    conductance='10pS',
                                    species=ion)

        chan.annotation = neuroml.Annotation()
        target = chan.gate_hh_tau_infs

        for gate in bio_params['gate_params']:

            gate_name = gate
            instances = bio_params['gate_params'][gate_name]['power']
            g_type='HHSigmoidVariable'

            g = neuroml.GateHHTauInf(id=gate_name, instances=instances)

            if gate_name == 'vda':
                v_half = str(channel_params['v_half_a']) + ' ' + str(unit['v_half_a'])
                k = str(channel_params['k_a']) + ' ' + str(unit['k_a'])
                g.steady_state = neuroml.HHTime(midpoint=v_half,scale=k,rate=1,type=g_type)
                if 'T_a' in channel_params:
                    T = str(channel_params['T_a']) + ' ' + str(unit['T_a'])
                    t_type="fixedTimeCourse"
                    g.time_course = neuroml.HHTime(tau=T, type=t_type)
            elif gate_name == 'vdi':
                v_half = str(channel_params['v_half_i']) + ' ' + str(unit['v_half_i'])
                k = str(channel_params['k_i']) + ' ' + str(unit['k_i'])
                g.steady_state = neuroml.HHTime(midpoint=v_half,scale=k,rate=1,type=g_type)
                if 'T_i' in channel_params:
                    T = str(channel_params['T_i']) + ' ' + str(unit['T_i'])
                    t_type="fixedTimeCourse"
                    g.time_course = neuroml.HHTime(tau=T, type=t_type)

            # TODO: Consider ion dependent activation/inactivation

            target.append(g)

        nml2_file_name = model_params['file_name']
        doc.ion_channel_hhs.append(chan)
        doc.id = channel_id
        writers.NeuroMLWriter.write(doc,nml2_file_name)

        print("Written NeuroML 2 channel file to: "+nml2_file_name)

        nml2_file = open(nml2_file_name, 'r')
        orig = nml2_file.read()
        new_contents = orig.replace("<annotation/>", "\n        <annotation>\n%s        </annotation>\n"%metadata.to_xml("            "))
        nml2_file.close()
        nml2_file = open(nml2_file_name, 'w')
        nml2_file.write(new_contents)
        nml2_file.close()

        myValidator = validators.Validator()
        myValidator.validate_nml2(nml2_file_name)

        return nml2_file

    def run_nml2(self,nml2_file):
        """

        :return:
        """

        return NML2ChannelAnalysis.run(channel_files=[nml2_file],nogui=False)
