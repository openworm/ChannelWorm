# ChannelWorm

The aim of **ChannelWorm** is to build
quantitative models of ion channel behavior in _C. elegans_ neurons.  The resulting models are exported to [**PyOpenWorm**](https://github.com/openworm/pyopenworm), OpenWorm's data access layer for storing both static physiological information as well as dynamic models about the nematode.  Ultimately, these models are used by [**c302**](https://github.com/openworm/c302) for simulating nervous system dynamics.  

## Installation
There are currently no installation scripts.  Simply clone the repository to begin working with the data and associated code.

## Objectives
* **Information Management of Primary Data Sources**
  * Integrate and structure data related to ion channels in _C. elegans_, from genotype to phenotype.  
  * Develop APIs for accessing data.  
  * Regularly curate data to ensure data quality.  
  * Develop collaborations with academic labs to collect new data.  
* **Ion channel modeling**
  * Build Hodgkin-Huxley models for ion channels based on experimental patch clamp studies.  
  * Estimate kinetics for ion channels with no patch clamp data available based on homologous channel types.  
  * Create verification & validation tests to prove matching of the models with experimental data using SciUnit.  
* **Integration with Simulation Platform**
  * Export models in NeuroML2 for storage in [PyOpenWorm](https://github.com/openworm/pyopenworm).
  * Build data access pipeline for [c302](https://github.com/openworm/c302) to access ion channel models from [PyOpenWorm](https://github.com/openworm/pyopenworm).  

## Repository Contents
* docs/- documentation for plot digitization, parameter extraction, and validation tools.  Deployed to [channelworm.readthedocs.io](https://channelworm.readthedocs.io)
* legacy/- contents of previous iteration of ChannelWorm repository.  See associated issues and milestones for tasks related to incorporating this work into the current setup.
* parameter_fitting/- genetic algorithms for extracting parameters for Hodgkin-Huxley type ion channel models.
* raw_data/- spreadsheets with curated data about ion channels, relevant plots from publications, and digitized time series to be used for parameter extraction.
* NML2_models/- NeuroML2 files generated from the parameter fitting process.
* tutorials_etc/- learning resources for ion channel modeling.  

## Release Notes
* _8/22/2018_: Major restructuring of repository.  Previous version of ChannelWorm has been moved to legacy folder.  New structure is organized around the raw data exported from [Chopen](chopen.herokuapp.com).  
