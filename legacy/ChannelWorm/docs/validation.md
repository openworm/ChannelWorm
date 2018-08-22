Validation
==========

The process of validation is *central* to OpenWorm's tenet of modeling with biological realism.
Only through comparing data produced by our simulations with data from the actual organism can we make the claim that we are modeling what we say we are.

This is as true for small-scale components of the worm as it is for the worm itself, and is thus important for ChannelWorm's goal of modeling *C. elegans* ion channels.

## The process - High level

[![](https://docs.google.com/drawings/d/13JvpUktlTXN2GKH9fXzacXQWudm5MQUMXXY94cr6S50/pub?w=778&h=370)](https://docs.google.com/drawings/d/13JvpUktlTXN2GKH9fXzacXQWudm5MQUMXXY94cr6S50/edit)

The modeling-validation-optimization loop is outlined in the diagram above, but the focus of this article is the validation step (green in the diagram).

At its core, the validation process relies on **comparing two sets of data**, one being the output of our [*simulated* ion channel experiments](simulation/), the other from *actual* ion channel experiments (ex: [digitized I/V plots](digitization/)).

Using the [SciUnit](https://github.com/scidash/sciunit) framework, tests are constructed to judge whether simulations of our models are close enough, on various parameters, to the observed data.

Depending on the results of these validation tests, the model will either be accepted or rejected. If the model is accepted, we [store it in a database](information-management/#data-management) with the supporting experimental evidence. If the model is rejected, we subject it to [further optimization](optimization/) and another round of simulation/validation testing. This loop continues until validation is passed, and the model is kept.

## Implementation

*Note:*Steps that are not yet streamlined will be tagged with their relevant Github issues. The details of these steps will be added as the issues are resolved.

### Inputs

* [Ion channel model data must be comparable to experimental data](https://github.com/VahidGh/ChannelWorm/issues/28)
* Model and experimental data should be pulled from the database (PyOpenWorm)

### Tests

* [A list of tests that can be run on the collection of models](https://github.com/VahidGh/ChannelWorm/issues/32)
* [A validation test template including testing (CI) environment](https://github.com/VahidGh/ChannelWorm/issues/27)
* Comparison of two sets of data using statistical tests, with numerical output

### Outputs

* Comparison of test output with "acceptable range", to determine whether the model is a good fit
* Ability to export data to database
* Ability to export data to optimization process
