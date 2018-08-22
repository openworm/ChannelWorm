Information Management
======================

An information management system is needed in order to:

-   Integrate data related to ion channels in C. elegans from different sources
-   Structure data for better representation
-   Ease access to the data through scripts/APIs
-   Keep data up-to-date

Data includes:

-   Description about the ion channel
-   Genetics, gene ontology, sequences, and locations
-   Proteins, structures, and homology information
-   Expression information and patterns in neurons/cells
-   Phenotypes and functionalities
-   Interaction network
-   Channelopathies (ion channel diseases), known mutations, and pharmacological studies
-   Available models and simulations
    -   Model type (from patch clamp studies, or estimation from known homologs)
    -   Experimental conditions (cell type, temperature, Reversal potential, age of the organism, etc.)
    -   Channel Properties (conductance, activation/inactivation parameters, etc.)
    -   Cell and synapse properties (membrane capacitance, surface area, external ion concentration, etc.)
    -   Graphs demonstrating kinetics
    -   Representation files for each model/simulation (NeuroML and LEMS respectively)
-   Evidence(s) for all the assertions

Data Collection
---------------

Biological information about each ion channel was obtained from the [WormBase](http://www.wormbase.org) database which is available in [this spread sheet file](https://docs.google.com/spreadsheet/ccc?key=0Avt3mQaA-HaMdEd6S0dfVnE4blhaY2ZIWDBvZFNjT0E#gid=1). Every tuple in the spread sheet has some links to its WormBase entry that could be used for more information.

![image](https://drive.google.com/uc?export=download&id=0B4qffTA1q81rUUw3ZlplY2ppTzA&authuser=0)

![image](https://drive.google.com/uc?export=download&id=0B4qffTA1q81raXUySG9vVTRXYTg)

In the *ion channels with properties* sheet, you can find properties, such as type, subtype, kinetic properties, etc. for every ion channel.

![image](https://drive.google.com/uc?export=download&id=0B4qffTA1q81rNnBYYjhlY2NVMmc)

The *references* column in this table contains links which reference publications on *Mendeley*.

![image](https://drive.google.com/uc?export=download&id=0B4qffTA1q81rbkZMVUhmXzVHTlE)

Data Management
---------------

To keep data in a structured and easy-to-access format, we use the [PyOpenWorm](https://github.com/openworm/PyOpenWorm), from the OpenWorm project. The database stores data for generating model files along with annotations describing the origins of the data. PyOpenWorm utilizes [RDF](http://pyopenworm.readthedocs.org/en/alpha0.5/process.html#why-rdf) which facilitates integration of data from disparate sources. For example, it is possible to ask PyOpenWorm to list all the ion channels of a muscle cell named MDL08, with evidence:

    muscle = PyOpenWorm.Muscle('MDL08')
    muscle.channels()
    ['EGL-19', 'SHK-1', 'SHL-1']
    #look up what reference says this muscle has an ion channel EGL-19
    muscle.get_reference(0,'EGL-19')
    ['http://dx.doi.org/10.1083%2Fjcb.200203055']

PyOpenWorm allows easy access to data about ion channels, either for human or machine reading.

For full usage of the PyOpenWorm API, take a look at [this document](http://travs-pyopenworm.readthedocs.org/en/channelworm/api.html)

Data Representation
-------------------

Final models are represented in [NeuroML2 format](http://www.neuroml.org/neuromlv2) which is an XML based description language that provides a common data format for defining and exchanging descriptions of neuronal cell and network models. You can find an example for this representation [here](https://github.com/VahidGh/ChannelWorm/blob/master/models/Kv1.channel.nml). Single channel kinetics are described by a NeuroML file, which could then be integrated with other channels and properties in a [LEMS](http://www.neuroml.org/lems_dev) format for final simulations ([LEMS sample file](https://github.com/openworm/muscle_model/blob/master/NeuroML2/LEMS_NeuronMuscle.xml)). For more information see [this tutorial](https://github.com/openworm/hodgkin_huxley_tutorial/).

In addition to [jNeuroML,](https://github.com/NeuroML/jNeuroML) these representation files could be used in [different tools](http://www.neuroml.org/tool_support) that support neuronal simulation. [Here](https://github.com/openworm/muscle_model/#21-simulation-of-muscle-cell-ion-channels) you can find an example for a simulation of muscle cell ion channels in C. elegans.

Finally an [XML file](https://raw.githubusercontent.com/dkruchinin/org.geppetto.samples/muscle_model/LEMS/MuscleModel/GEPPETTO.xml) could be generated for running the simulation under the [Geppetto simulator](https://github.com/openworm/org.geppetto).

Update Management
-----------------

In order to get informed about new publications about ion channels in C. elegans and also any update on existing data, an update management system should be implemented.

### Current State

You can find open/closed issues for this topic [here](https://github.com/VahidGh/ChannelWorm/milestones/Data%20Collection%20And%20Management)
