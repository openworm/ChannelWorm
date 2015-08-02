# ChannelWorm
 
[![Documentations](https://readthedocs.org/projects/channelworm/badge/?version=latest)](http://channelworm.readthedocs.org/en/latest/) [![Join the chat at https://gitter.im/VahidGh/ChannelWorm](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/openworm/ChannelWorm?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Stories in Ready](https://badge.waffle.io/vahidgh/channelworm.png?label=ready&title=Ready)](https://waffle.io/vahidgh/channelworm) [![Build Status](https://travis-ci.org/openworm/ChannelWorm.svg?branch=dev)](https://travis-ci.org/openworm/ChannelWorm)

The aim of the **ChannelWorm** is to integrate information and tools related to modeling ion channels in C. elegans for the [OpenWorm Project](https://github.com/openworm).

## Installation

To install this project, just clone it locally and do `pip install -r requirements.txt'

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

## Implementation

As part of the OpenWorm's Muscle-Neuron-Channel [integration plan](http://docs.openworm.org/en/latest/Projects/muscle-neuron-integration/), ChannelWorm is developing based on the following components:

   * The [PyOpenWorm](https://github.com/openworm/PyOpenWorm) is the main data layer API for the knowledge base.
   * The [Django app](http://channelwormdjango-channelworm.rhcloud.com/) is being used as an interface for digitization, data representation and user interaction.
   * Collected data fits to dynamic models using [cwFitter](https://github.com/openworm/ChannelWorm/tree/master/channelworm/fitter) optimization engine.
   * Using the OpenWorm's unittesting framework, verification tests are applied, and models are validated by [SciUnit](https://github.com/scidash/sciunit).
   * Final models are generated in [NeuroML2](https://github.com/NeuroML) format, in addition to [LEMS](https://github.com/LEMS) files for simulation environments.
   * Verified models and simulations can be run in the [Geppetto](https://github.com/openworm/org.geppetto) simulation platform.
 

