# ChannelWorm

The aim of the **ChannelWorm** is to integrate information and tools related to modeling ion channels in C. elegans for the [OpenWorm Project](https://github.com/openworm).

## Objectives
* **Information Management**
  * Integrate and structure data related to ion channels in C. elegans, from genotype to phenotype
  * Develop APIs for accessing data
  * Keep data up-to-date
* **Ion channel modeling**
  * Build Hodgkin-Huxley models for ion channels based on experimental patch clamp studies
  * Estimate kinetics and build models for ion channels with no patch clamp data available (based on homologous channel types)
  * Create verification & validation tests to prove matching of the models with experimental data
* **Setting up a simulation environment**
  * Simulate the computational analysis phase of a patch clamp experiment
  * Simulate and run customized versions of ion channel(s) in cell(s)
  * Check if the simulation fits the biological boundaries

## Some use cases
  * I want to know which type of ion channels we have in C. elegans!
  * I want to know in which cell which gene encodes which protein/subtype of which ion channel!
  * I want to view, build, or validate a model of an ion channel
  * I want to check references that data or models are based on
  * I have some graphs/data from a patch clamp experiment and want to build a HH model
  * I want to have a customized version of an ion channel model (e.g. of a mutant)
  * I want to run my customized model of ion channel(s) (along with other ion channels) in a simulation environment
  * I want to simulate a patch clamp experiment with known mutations in genes encoding ion channels in C. elegans
  * I want to simulate ion channel diseases (channelopathies), and investigate defects in neuromuscular transmission, C. elegans movement, etc.

**Note:** All the models are generated in [NeuroML2](https://github.com/NeuroML) format and all the simulations in [LEMS](https://github.com/LEMS), and the verified models can be run in the [Geppetto](https://github.com/openworm/org.geppetto) simulation platform.
 
 
Click [**here**](http://channelworm.readthedocs.org/en/latest/intro.html) for more information.
 
 [![Join the chat at https://gitter.im/VahidGh/ChannelWorm](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/VahidGh/ChannelWorm?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
