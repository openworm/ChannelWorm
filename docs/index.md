Introduction
============

Ion channels are pore-forming proteins, found in the membranes of all cells. Their known functions include establishing a resting membrane potential, shaping electrical signals like action potentials, gating the flow of ions across the cell membrane, controlling cell volume, and regulating the net flow of ions across epithelial cells of secretory and resorptive tissues. Ion channels are considered to be one of the two traditional classes of ionophoric proteins, with the other class known as ion transporters (including the sodium-potassium pump, sodium-calcium exchanger, and sodium-glucose transport proteins, amongst others). <sup>[[1]](#ref1)</sup>

Most plasma membrane ion channels in the nervous system come in four distinct topologies which likely evolved independently <sup>[[2]](#ref2)</sup> :

-   The voltage-gated family of potassium, sodium and calcium channels
-   The cysteine-loop family of ligand-gated ion channels
-   Ionotropic glutamate receptors
-   P2X and ASIC channels

The C. elegans genome codes for members of all the main families of ion channels. Within specific families, there are some individual members missing, the most notable being sodium-gated ion channels, P2X channels and HCN channels.

![image](https://drive.google.com/uc?export=download&id=0B4qffTA1q81rZkhCaTNWVk5mYjQ)

Ion channels, and associated regulatory machinery have been identified in genetic screens of various processes in C. elegans such as locomotion, gonad development, mechanosensory and osmotic avoidance behavior, chemotaxis and thermotaxis, resistance to fluoride ions, defecation, egg laying, toxin and heavy metal sensitivity, programmed cell death, neuronal degeneration, and abnormal catecholamine levels.

A wealth of powerful molecular tools and online databases are available to study ion channels and transporter functional genomics in C. elegans. Conceptually, functional genomic studies can be divided into two approaches.

The gene-driven approach focuses on identification, cloning, and characterization of genes. Gene characterization involves expression and structure-function studies and determination of where and when a gene is expressed in the organism.

The phenotype-driven approach seeks to determine the physiological roles of genes from the cellular to whole animal level, and to identify the mechanisms that regulate protein function. <sup>[[3]](#ref3)</sup>

ChannelWorm
===========

Due to its simplicity and wealth of data available, C. elegans is an ideal organism for modeling ion channels and related functionalities. The aim of the **ChannelWorm** is to integrate information and tools related to modeling ion channels in C. elegans for the [OpenWorm Project](https://github.com/openworm). Here we use the Hodgkin Huxley approach for modeling ion channel kinetics and simulating action potentials in excitable cells in C. elegans (see [this tutorial](http://hodgkin-huxley-tutorial.readthedocs.org/en/latest/_static/Tutorial.html)).

Objectives
==========

-   **Information management**
    -   Integrate and structure data related to ion channels in C. elegans, from genotype to phenotype
    -   Develop APIs for accessing data
    -   Keep data up-to-date
-   **Ion channel modeling**
    -   Build Hodgkin-Huxley models for ion channels based on experimental patch clamp studies
    -   Estimate kinetics and build models for ion channels with no patch clamp data available (based on homologous channel types)
    -   Create verification & validation tests to prove matching of the models with experimental data
-   **Setting up a simulation environment**
    -   Simulate the computational analysis phase of a patch clamp experiment
    -   Simulate and run customized versions of ion channel(s) in cell(s)
    -   Check if the simulation fits the biological boundaries

Some use cases
==============

-   I want to know which type of ion channels we have in C. elegans!
-   I want to know in which cell which gene encodes which protein/subtype of which ion channel!
-   I want to view, build, or validate a model of an ion channel
-   I want to check references that data or models are based on
-   I have some graphs/data from a patch clamp experiment and want to build a HH model
-   I want to have a customized version of an ion channel model (e.g. of a mutant)
-   I want to run my customized model of ion channel(s) (along with other ion channels) in a simulation environment
-   I want to simulate a path clamp experiment with known mutations in genes encoding ion channels in C. elegans
-   I want to simulate ion channel diseases (channelopathies), and investigate defects in neuromuscular transmission, C. elegans movement, etc.

Implementation
==============

All the models are generated in [NeuroML2](https://github.com/NeuroML) format and all the simulations in [LEMS](https://github.com/LEMS), and the verified models can be run in the [Geppetto](https://github.com/openworm/org.geppetto) simulation platform.

References
----------

1. <a name="ref1"></a> Hille, Bertil (1984). Ionic Channels of Excitable Membranes.
2. <a name="ref2"></a> Hobert O. The neuronal genome of Caenorhabditis elegans (August 13, 2013), WormBook, ed. The C. elegans Research Community, WormBook, doi/10.1895/wormbook.1.161.1, http://www.wormbook.org.
3. <a name="ref3"></a> Kevin Strange. From Genes to Integrative Physiology: Ion Channel and Transporter Biology in Caenorhabditis elegans, Physiological Reviews, Apr 2003, 83 (2) 377-415; DOI: 10.1152/physrev.00025.2002
