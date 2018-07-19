# ChannelWorm

[![Build Status](https://travis-ci.org/openworm/ChannelWorm.svg?branch=dev)](https://travis-ci.org/openworm/ChannelWorm)

The aim of **ChannelWorm** is to build
quantitative models of ion channel behavior in _C. elegans_ neurons.  The resulting models are exported to [**PyOpenWorm**](https://github.com/openworm/pyopenworm), OpenWorm's data access layer for storing both static physiological information as well as dynamic models about the nematode.  Ultimately, these models are used by [**c302**](https://github.com/openworm/c302) for simulating nervous system dynamics.  

## Installation

To install this project, clone it locally with `git` and run `pip install -r requirements.txt` at a console.
Please be sure to look at the contents of `requirements.txt` for certain dependencies cannot be installed automatically via `pip`.

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
  * Export models in NeuroML2 for storage in PyOpenWorm.
  * Built data access pipeline for c302 to access ion channel models from PyOpenWorm.  

## Repository contents
* channelworm/
* data/- spread sheet with extensive curated information about ion channels
* docs/ Documentation for plot digitization, parameter extraction, and validation tools.  
* models/ NeuroML2 files generated from the parameter fitting process.  These are temporarily housed here, but will ultimately be accessed by the simulation platform through [PyOpenWorm](https://github.com/openworm/pyopenworm).  
* scripts/
* tests/ standard software tests as well as model validation tests. Some of the tests in this folder are unit / integration tests.  The model validation tests in the Python framework [SciUnit](https://github.com/scidash/sciunit) have now been moved to a separate, project-wide repository for housing and running model validation tests, simply called [openworm/tests](https://github.com/openworm/tests).  
