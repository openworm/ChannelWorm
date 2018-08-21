# Ion Channel Fitter For OpenWorm

<img src="https://github.com/gsarma/ion_channel_fitting/blob/images/EGL-19.png?raw=tru" height="400">

This repository contains implementations of the techniques described in the paper by Gurkeiwicz and Korngreen ["A Numerical Approach to Ion Channel
Modelling Using Whole-Cell Voltage-Clamp
Recordings and a Genetic Algorithm"](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.0030169).

I currently have implementations in both the Wolfram Language and Python. These are mostly
intended to be used for learning the essentials of the techniques and not for out-of-the-box use.  

## Contents:

* data/EGL-19_patch_clamp.csv: times series for EGL-19 ion channel

* notes/genetic_algorithm_notes*: notes explaining some details of the implementation

* WL/ionChannelFitter.wl: Wolfram Language implementation of genetic algorithm for parameter extraction.  

* WL/EGL-19.nb: Wolfram Language notebook for EGL-19 voltage gated calcium channel

* python/EGL-19.ipynb: Jupyter notebook with Python implementation
