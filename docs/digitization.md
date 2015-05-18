Digitization
============

Digitized figures from papers in the literature will be used to validate the ion channel models of ChannelWorm.

For example, a study which conducts [patch clamp recordings](https://en.wikipedia.org/wiki/Patch_clamp) will produce data that describe electrical properties of ion channels.
This data is valuable to anyone modeling these ion channels; we can use actual ion channel data to guide our efforts toward biological realism, and incorporate it in [confirming that we are modeling what we are intending to](validation/).

## So why digitization?

In a published paper, data is included in an expressive form, such as a visual plot, rather than as raw numerical data. This is not to say that we cannot *extract* the information and make use of it, however.

Using [digitization programs](http://arohatgi.info/WebPlotDigitizer/), it is possible to reconstruct the numerical data from a graph, which is much more usable for our purposes of validation and optimization.

![](https://cloud.githubusercontent.com/assets/6655104/6027361/b509831c-abf6-11e4-95a4-372b911533fb.png)

In the above example, an [I/V curve](https://en.wikipedia.org/wiki/Current%E2%80%93voltage_characteristic) from a journal article was digitized to get back [data](https://plot.ly/~VahidGh/56) describing an important electrical property of an ion channel. It is easy to imagine how this type of data might now be used in other aspects of our *in silico* ion channel models.

## In more detail

[![](https://docs.google.com/drawings/d/1MDAJkv1wXJTmr5ux0EDvlz5xkUz13ez3YIJ6fmSMpms/pub?w=730&h=461)](https://docs.google.com/drawings/d/1MDAJkv1wXJTmr5ux0EDvlz5xkUz13ez3YIJ6fmSMpms/edit)

Starting out, the goal is to construct and maintain [a list of ion channels](https://github.com/VahidGh/ChannelWorm/issues/8) relevant to *C. elegans*, and a corresponding list of papers with data plots relevant to each of these ion channels.

Once a collection of such papers is compiled, figures describing the ion channels in question must be extracted as image files.

These image files can then be processed by [digitization software](http://arohatgi.info/WebPlotDigitizer/), which will return datapoints that can be stored in [the project's centralized database](information-management/#data-management) for later retrieval.
