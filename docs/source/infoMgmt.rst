************************
Information Management
************************

In order to integrate data related to ion channels in C. elegans from different sources, structure data for better 
representation, ease of access from different scripts and APIs, and finally keep them up-to-date, an information management 
system is needed.

Data includes:

* Description about the ion channel
* Genetics, Gene Ontology, sequences, and locations
* Proteins, structures, and homology information
* Expression information and pattern in neurons/cells
* Phenotypes and functionalities
* Interaction network
* Channelopathies (ion channel diseases), known mutations, and pharmacological studies
* Available models and simulations

  * Model type (from patch clamp studies, or estimation from known homologs)
  * Experimental conditions (cell type, temperature, Reversal potential, age of the cell, etc.)
  * Channel Properties (conductance, activation/inactivation parameters, etc.)
  * Cells and synapses properties (membrane capacitance, surface area, external ion concentration, etc.)
  * Graphs demonstrating kinetics
  * Representation files for each model/simulation

* Evidence(s) for all the assertions

Data Collection
===============
In the first attempt, biological information about each ion channel obtained from the `WormBase <http://www.wormbase.org>`_ database which is available in 
`this spread sheet file <https://docs.google.com/spreadsheet/ccc?key=0Avt3mQaA-HaMdEd6S0dfVnE4blhaY2ZIWDBvZFNjT0E#gid=1>`_. Every tuple in the spread sheet has some links to its WormBase entry that could be used for more information.

.. image:: https://drive.google.com/uc?export=download&id=0B4qffTA1q81rUUw3ZlplY2ppTzA&authuser=0
.. image:: https://drive.google.com/uc?export=download&id=0B4qffTA1q81raXUySG9vVTRXYTg 

In the *ion channels with properties* section, you can find properties, such as type, subtype, kinetic properties, etc. for every ion channel.

.. image:: https://drive.google.com/uc?export=download&id=0B4qffTA1q81rNnBYYjhlY2NVMmc

The *references* column in this table, contains links which by following, you can access reference publications on *Mendeley*.

.. image:: https://drive.google.com/uc?export=download&id=0B4qffTA1q81rbkZMVUhmXzVHTlE


Data Management
===============
To keep data in a more structured and easy-to-access way, we use the `PyOpenWorm <https://github.com/openworm/PyOpenWorm>`_, from the OpenWorm project
The database stores data for generating model files and together with annotations describing the origins of the data.
PyOpenWorm supports `RDF <http://pyopenworm.readthedocs.org/en/alpha0.5/process.html#why-rdf>`_ which facilitates integration of data from disparate sources.
For example, it is possible to ask PyOpenWorm to list all the ion channels of a muscle cell named MDL08, with evidences::

    muscle = PyOpenWorm.Muscle('MDL08')
    muscle.channels()
    ['EGL-19', 'SHK-1', 'SHL-1']
    #look up what reference says this muscle has an ion channel EGL-19
    muscle.get_reference(0,'EGL-19')
    ['http://dx.doi.org/10.1083%2Fjcb.200203055']

Data Representation
===================
Final models are represented in `NuroML2 format <http://www.neuroml.org/neuromlv2>`_ which is a XML based description language that provides a common data format 
for defining and exchanging descriptions of neuronal cell and network models. You can find an example for this representation `here <https://github.com/VahidGh/ChannelWorm/blob/master/models/Kv1.channel.nml>`_.
Single channel kinetics described by a NeuroML file, then could be integrated with other channels and properties in a `LEMS <http://www.neuroml.org/lems_dev>`_ format for final simulations (`LEMS sample file <https://github.com/openworm/muscle_model/blob/master/NeuroML2/LEMS_NeuronMuscle.xml>`_).
For more information see `this tutorial <https://github.com/openworm/hodgkin_huxley_tutorial/>`_.

In addition to `jNeuroML <https://github.com/NeuroML/jNeuroML>`_ these representation files could be used in `different tools <http://www.neuroml.org/tool_support>`_ that support neuronal simulation.
`Here <https://github.com/openworm/muscle_model/#21-simulation-of-muscle-cell-ion-channels>`_ you can find an example for a simulation of muscle cell ion channels in C. elegans.

Finally an `XML file <https://raw.githubusercontent.com/dkruchinin/org.geppetto.samples/muscle_model/LEMS/MuscleModel/GEPPETTO.xml>`_ could be generated for running the simulation under the `Geppetto simulator <https://github.com/openworm/org.geppetto>`_.

Update Management
=================
In order to get informed about new publications about ion channels in C. elegans and also any update on existing data, an update management system 
should be implemented.

Current State
-------------
You can find open/closed issues for this topic `here <https://github.com/VahidGh/ChannelWorm/milestones/Data%20Collection%20And%20Management>`_

