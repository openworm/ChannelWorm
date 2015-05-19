Optimization
============

As described in the [general OpenWorm documentation](http://docs.openworm.org/en/latest/Projects/optimization/), optimization is being employed at several levels of the project. By tuning the parameters of the models to experimental data, a high degree of biological realism can be attained.

## How ChannelWorm uses optimization

[![](https://docs.google.com/drawings/d/13JvpUktlTXN2GKH9fXzacXQWudm5MQUMXXY94cr6S50/pub?w=778&h=370)](https://docs.google.com/drawings/d/13JvpUktlTXN2GKH9fXzacXQWudm5MQUMXXY94cr6S50/edit)

At a high level, the modeling-validation-optimization loop relies on the optimization process to consume inaccurate models and return more accurate models, given some experimental objective data.

A model is chosen for optimization if it fails the [validation stage](validation/) of this loop. Inside the optimization process, the model's parameters are then tuned to minimize their difference with the experimental data used for validation.

A new model with slightly different parameters is produced, and is pulled into the validation stage once again. This loop continues until the validation stage is passed, and the model is finally [stored](information-management/#data-management).

## The process in detail

*Note:*Steps that are not yet streamlined will be tagged with their relevant Github issues. The details of these steps will be added as the issues are resolved.

### Inputs

* A hook must be established to import models that fail [validation](validation/)
* Will the optimization itself take place locally or on a remote machine?

### Optimization

* Selection of free parameters
* Selection of training data from simulated data
* What type of optimization algorithm will be used? There is material [here](https://drive.google.com/open?id=0B_t3mQaA-HaMbXA1M0s1a25KSTA&authuser=0) about genetic algorithms, and information [here](https://optimal-neuron.readthedocs.org/en/latest/architecture.html) on NeuroTune
* Scripts to perform the optimization will differ depending on the above choice

### Outputs

* Update the model's parameters with the results of the optimization
* Save the new model in a form that can be simulated again, to continue the loop
