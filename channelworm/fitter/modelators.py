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
import pickle
from numpy import random, abs, asarray
from pyneuroml.analysis import NML2ChannelAnalysis
from channelworm.fitter import validators

class Modelator(object):

    def __init__(self, bio_params, sim_params):

        self.cell_params = bio_params['cell_params']
        self.channel_params = bio_params['channel_params']
        self.sim_params = sim_params

    def patch_clamp_plots(self, simData, show=False, path=''):
        """
        Generates patch clamp plots for ion channel kinetics (I/t, Po/t, etc.)
        """

        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        i = 1

        it = plt.figure(i)
        for ind,trace in enumerate(simData['I']):
            plt.plot([i*1e3 for i in simData['t']],[j*1e12 for j in trace], color=random.rand(3,1), label='%i mV'%(simData['V_ss'][ind]*1e3))
        plt.legend(fontsize=9, bbox_to_anchor=(1., 0., 0.14, .101), loc=3, mode="expand", borderaxespad=0.)
        plt.title("Current versus Time")
        plt.xlabel("Time (ms)")
        plt.ylabel("Current (pA)")
        plt.savefig(path+"current_time.png",bbox_inches='tight',format='png')
        pickle.dump(it, file(path+"current_time.pickle", 'w'))
        if show:
            plt.draw()
        i+=1

        pot = plt.figure(i)
        for ind,trace in enumerate(simData['PO']):
            plt.plot([i*1e3 for i in simData['t']],trace, color=random.rand(3,1), label='%i mV'%(simData['V_ss'][ind]*1e3))
        plt.legend(fontsize=9, bbox_to_anchor=(1., 0., 0.14, .101), loc=3, mode="expand", borderaxespad=0.)
        plt.title("G/G_max versus Time")
        plt.xlabel("Time (ms)")
        plt.ylabel("G/G_max")
        plt.savefig(path+"GG_max_time.png",bbox_inches='tight',format='png')
        pickle.dump(pot, file(path+"GG_max_time.pickle", 'w'))
        if show:
            plt.draw()
        i+=2

        vt = plt.figure(i)
        for ind,trace in enumerate(simData['V']):
            plt.plot([i*1e3 for i in simData['t']],[j*1e3 for j in trace], color=random.rand(3,1), label='%i mV'%(simData['V_ss'][ind]*1e3))
        plt.legend(fontsize=9, bbox_to_anchor=(1., 0., 0.14, .101), loc=3, mode="expand", borderaxespad=0.)
        plt.title("Voltage versus Time")
        plt.xlabel("Time (ms)")
        plt.ylabel("Voltage (mV)")
        plt.savefig(path+"voltage_time.png",bbox_inches='tight',format='png')
        pickle.dump(vt, file(path+"voltage_time.pickle", 'w'))
        if show:
            plt.draw()
        i+=1

        if show:
            plt.show()

        return plt

    def gating_plots(self, simData, show=False, path=''):
        """
        Generates gating plots for ion channel kinetics (m, h, etc)
        """

        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        i = 1

        iv_ss = plt.figure(i)
        plt.plot([round(x*1e3) for x in simData['V_ss']],[j*1e12 for j in simData['I_ss']], color='b', label='Steady state current')
        plt.plot([round(x*1e3) for x in simData['V_ss']],[j*1e12 for j in simData['I_max']], color='r', label='Peak current')
        plt.legend(loc='best')
        plt.title("Current versus membrane potential")
        plt.xlabel("Voltage (mV)")
        plt.ylabel("Current (pA)")
        plt.savefig(path+"current_vs_voltage.png",bbox_inches='tight',format='png')
        pickle.dump(iv_ss, file(path+"current_vs_voltage.pickle", 'w'))
        if show:
            plt.draw()
        i+=1

        pov = plt.figure(i)
        plt.plot([round(x*1e3) for x in simData['V_ss']],[j for j in simData['PO_ss']], color='b', label='Steady state G/G_max')
        plt.plot([round(x*1e3) for x in simData['V_ss']],[j for j in simData['PO_max']], color='r', label='Peak G/G_max')
        plt.legend(loc='best')
        plt.title("G/G_max versus membrane potential")
        plt.xlabel("Voltage (mV)")
        plt.ylabel("G/G_max")
        plt.savefig(path+"GG_max_vs_voltage.png",bbox_inches='tight',format='png')
        pickle.dump(pov, file(path+"GG_max_vs_voltage.pickle", 'w'))
        if show:
            plt.draw()
        i+=1

        if 'm_inf' in simData:
            m = plt.figure(i)
            plt.plot([round(x*1e3) for x in simData['V_ss']],simData['m_inf'], color='b', label='m_inf')
            plt.legend(loc='best')
            plt.title("Steady state activation versus membrane potential")
            plt.xlabel("Voltage (mV)")
            plt.ylabel("Steady state activation")
            plt.savefig(path+"steadyStateAct_vs_voltage.png",bbox_inches='tight',format='png')
            pickle.dump(m, file(path+"steadyStateAct_vs_voltage.pickle", 'w'))
            if show:
                plt.draw()
            i+=1

        if 'h_inf' in simData:
            h = plt.figure(i)
            plt.plot([round(x*1e3) for x in simData['V_ss']],simData['h_inf'], color='r', label='h_inf')
            plt.legend(loc='best')
            plt.title("Steady state inactivation versus membrane potential")
            plt.xlabel("Voltage (mV)")
            plt.ylabel("Steady state inactivation")
            plt.savefig(path+"steadyStateInact_vs_voltage.png",bbox_inches='tight',format='png')
            pickle.dump(h, file(path+"steadyStateInact_vs_voltage.pickle", 'w'))
            if show:
                plt.draw()
            i+=1

        if 'cdi_inf' in simData:
            cdi = plt.figure(i)
            plt.plot([round(x*1e3) for x in simData['V_ss']],simData['cdi_inf'], color='y', label='Ca-dependent inactivation')
            plt.legend(loc='best')
            plt.title("Steady state Calcium-dependent inactivation versus membrane potential")
            plt.xlabel("Voltage (mV)")
            plt.ylabel("Steady state Calcium-dependent inactivation")
            plt.savefig(path+"steadyStateCdi_vs_voltage.png",bbox_inches='tight',format='png')
            pickle.dump(cdi, file(path+"steadyStateCdi_vs_voltage.pickle", 'w'))
            if show:
                plt.draw()
            i+=1

        if 'm_tau' in simData:
            mt = plt.figure(i)
            plt.plot([round(x*1e3) for x in simData['V_ss']],[round(x*1e3) for x in simData['m_tau']], color='b', label='m_tau')
            plt.legend(loc='best')
            plt.title("Time constant of activation versus membrane potential")
            plt.xlabel("Voltage (mV)")
            plt.ylabel("Time constant of activation (ms)")
            plt.savefig(path+"mtau_vs_voltage.png",bbox_inches='tight',format='png')
            pickle.dump(mt, file(path+"mtau_vs_voltage.pickle", 'w'))
            if show:
                plt.draw()
            i+=1

        if 'h_tau' in simData:
            th = plt.figure(i)
            plt.plot([round(x*1e3) for x in simData['V_ss']],[round(x*1e3) for x in simData['h_tau']], color='r', label='h_tau')
            plt.legend(loc='best')
            plt.title("Time constant of inactivation versus membrane potential")
            plt.xlabel("Voltage (mV)")
            plt.ylabel("Time constant of inactivation (ms)")
            plt.savefig(path+"htau_vs_voltage.png",bbox_inches='tight',format='png')
            pickle.dump(th, file(path+"htau_vs_voltage.pickle", 'w'))
            if show:
                plt.draw()
            i+=1

        if show:
            plt.show()

        return plt

    def compare_plots(self, sampleData, simData, show=False, path=''):
        """
        Generates originals vs simulated plots
        """

        i = 1

        if 'VClamp' in sampleData:
            flag = False
            vc = plt.figure(i)
            ref = sampleData['VClamp']['ref']
            x_var = sampleData['VClamp']['x_var']
            y_var = sampleData['VClamp']['y_var']
            for trace in sampleData['VClamp']['traces']:
                sample_plot, = plt.plot([i/x_var['toSI'] for i in trace['t']],[j/y_var['toSI'] for j in trace['I']], '--ko')
                off = self.sim_params['end_time']
                offset = abs(asarray(trace['t'])-off).argmin()

                if 'vol' in trace and trace['vol']:
                    plt.text(trace['t'][offset]/x_var['toSI']+10, trace['I'][offset]/y_var['toSI'], '%i mV'%(trace['vol']*1e3), color='k')

                    index = abs(simData['V_ss'] - trace['vol']).argmin()
                    model_plot, = plt.plot([i/x_var['toSI'] for i in simData['t']],[j/y_var['toSI'] for j in simData['I'][index]], color='r')
                    flag = True

            if flag is False:
                for ind,trace in enumerate(simData['I']):
                    off = self.sim_params['end_time']
                    offset = abs(asarray(trace['t'])-off).argmin()
                    plt.text(simData['t'][offset]/x_var['toSI']+10, trace[offset]/y_var['toSI'], '%i mV'%(simData['V_ss'][ind]*1e3), color='k')
                    plt.plot([i/x_var['toSI'] for i in simData['t']],[j/y_var['toSI'] for j in trace], color='r')

            plt.legend([sample_plot,model_plot],
                       ["Digitized data from Fig.%s, DOI: %s" %(ref['fig'],ref['doi']),"Best fit"],
                       bbox_to_anchor=(0., 1.01, 1., .101), loc=3,ncol=2, mode="expand", borderaxespad=0., fontsize=10)
            plt.title("The Best Model fitted to data for voltage-clamp experiment", y=1.05)
            plt.xlabel('%s (%s)'%(x_var['type'],x_var['unit']))
            plt.ylabel('%s (%s)'%(y_var['type'],y_var['unit']))
            plt.savefig(path+"data_vs_candidate-VClamp.png",bbox_inches='tight',format='png')
            pickle.dump(vc, file(path+"data_vs_candidate-VClamp.pickle", 'w'))

            if show:
                plt.draw()
            i+=1

        if 'IClamp' in sampleData:
            ic = plt.figure(i)
            ref = sampleData['IClamp']['ref']
            x_var = sampleData['IClamp']['x_var']
            y_var = sampleData['IClamp']['y_var']
            for trace in sampleData['IClamp']['traces']:
                if 'amp' in trace and trace['amp']:
                    sample_plot, = plt.plot([i/x_var['toSI'] for i in trace['t']],[j/y_var['toSI'] for j in trace['V']],
                                            '--ko', label = '%i (uA)'%(trace['amp']*1e6))
                else:
                    sample_plot, = plt.plot([i/x_var['toSI'] for i in trace['t']],[j/y_var['toSI'] for j in trace['V']], '--ko')

            amp = self.sim_params['protocol_end']
            for trace in simData['V']:
                model_plot, = plt.plot(simData['t'],trace, color='r')
                amp -= self.sim_params['protocol_steps']

            plt.legend([sample_plot,model_plot],
                       ["Digitized data from Fig.%s, DOI: %s"%(ref['fig'],ref['doi']),"Best fit"],
                       bbox_to_anchor=(0., 1.01, 1., .101), loc=3,ncol=2, mode="expand", borderaxespad=0., fontsize=10)
            plt.title("The best model fitted to data for current-clamp experiment", y=1.06)
            plt.xlabel('%s (%s)'%(x_var['type'],x_var['unit']))
            plt.ylabel('%s (%s)'%(y_var['type'],y_var['unit']))
            plt.savefig(path+"data_vs_candidate-IClamp.png",bbox_inches='tight',format='png')
            pickle.dump(ic, file(path+"data_vs_candidate-IClamp.pickle", 'w'))

            if show:
                plt.draw()
            i+=1

        if 'IV' in sampleData:
            iv = plt.figure(i)
            ref = sampleData['IV']['ref']
            x_var = sampleData['IV']['x_var']
            y_var = sampleData['IV']['y_var']
            if 'I_peak' in sampleData['IV']:
                sample_plot, = plt.plot([i/x_var['toSI'] for i in sampleData['IV']['V']],
                                        [j/y_var['toSI'] for j in sampleData['IV']['I_peak']],'--ko')
                model_plot, = plt.plot([i/x_var['toSI'] for i in simData['V_max']],
                                       [j/y_var['toSI'] for j in simData['I_max']],'r')
            else:
                sample_plot, = plt.plot([i/x_var['toSI'] for i in sampleData['IV']['V']],
                                        [j/y_var['toSI'] for j in sampleData['IV']['I']],'--ko')
                model_plot, = plt.plot([i/x_var['toSI'] for i in simData['V_ss']],
                                       [j/y_var['toSI'] for j in simData['I_ss']],'r')
            plt.legend([sample_plot,model_plot],
                       ["Digitized data from Fig.%s, DOI: %s"%(ref['fig'],ref['doi']),"Best fit"],
                       bbox_to_anchor=(0., 1.01, 1., .101), loc=3,ncol=2, mode="expand", borderaxespad=0., fontsize=10)
            plt.title("The Best Model fitted to data for I/V curve", y=1.06)
            plt.xlabel('%s (%s)'%(x_var['type'],x_var['unit']))
            plt.ylabel('%s (%s)'%(y_var['type'],y_var['unit']))
            plt.savefig(path+"data_vs_candidate-IV.png",bbox_inches='tight',format='png')
            pickle.dump(iv, file(path+"data_vs_candidate-IV.pickle", 'w'))

            if show:
                plt.draw()
            i+=1

        if 'POV' in sampleData:
            pov = plt.figure(i)
            ref = sampleData['POV']['ref']
            x_var = sampleData['POV']['x_var']
            y_var = sampleData['POV']['y_var']
            if 'PO_peak' in sampleData['POV']:
                sample_plot, = plt.plot([i/x_var['toSI'] for i in sampleData['POV']['V']],
                                        [j/y_var['toSI'] for j in sampleData['POV']['PO_peak']],'--ko')
                model_plot, = plt.plot([i/x_var['toSI'] for i in simData['V_PO_max']],
                                       [j/y_var['toSI'] for j in simData['PO_max']],'r')
            else:
                sample_plot, = plt.plot([i/x_var['toSI'] for i in sampleData['POV']['V']],
                                        [j/y_var['toSI'] for j in sampleData['POV']['PO']],'--ko')
                model_plot, = plt.plot([i/x_var['toSI'] for i in simData['V_ss']],
                                       [j/y_var['toSI'] for j in simData['PO_ss']],'r')
            plt.legend([sample_plot,model_plot],
                       ["Digitized data from Fig.%s, DOI: %s"%(ref['fig'],ref['doi']),"Best fit"],
                       bbox_to_anchor=(0., 1.01, 1., .101), loc=3,ncol=2, mode="expand", borderaxespad=0., fontsize=10)
            plt.title("The Best Model fitted to data for G/Gmax / V curve", y=1.06)
            plt.xlabel('%s (%s)'%(x_var['type'],x_var['unit']))
            plt.ylabel('%s (%s)'%(y_var['type'],y_var['unit']))
            plt.savefig(path+"data_vs_candidate-POV.png",bbox_inches='tight',format='png')
            pickle.dump(pov, file(path+"data_vs_candidate-POV.pickle", 'w'))

            if show:
                plt.draw()
            i+=1

        if show:
            plt.show()

        return plt

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
