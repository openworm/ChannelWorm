Digitization
============

Digitized figures from papers in the literature will be used to validate the ion channel models of ChannelWorm.

For example, a study which conducts [patch clamp recordings](https://en.wikipedia.org/wiki/Patch_clamp) will produce data that describe electrical properties of ion channels.
This data is valuable to anyone modeling these ion channels; we can use actual ion channel data to guide our efforts toward biological realism, and incorporate it in [confirming that we are modeling what we are intending to](validation/).

## So why digitization?

In a published paper, data is included in an expressive form, such as a visual plot, rather than as raw numerical data. This is not to say that we cannot *extract* the information and make use of it, however.

Using [digitization programs](http://arohatgi.info/WebPlotDigitizer/), it is possible to reconstruct the numerical data from a graph, which is much more usable for our purposes of validation and optimization.

<iframe width="640" height="480" frameborder="0" seamless="seamless" scrolling="no" src="https://plot.ly/~VahidGh/56/" ></iframe>

In the above example, an [I/V curve](https://en.wikipedia.org/wiki/Current%E2%80%93voltage_characteristic) from a journal article was digitized to get back [data](https://plot.ly/~VahidGh/56) describing an important electrical property of an ion channel. It is easy to imagine how this type of data might now be used in other aspects of our *in silico* ion channel models.

## In more detail

[![](https://docs.google.com/drawings/d/1MDAJkv1wXJTmr5ux0EDvlz5xkUz13ez3YIJ6fmSMpms/pub?w=730&h=461)](https://docs.google.com/drawings/d/1MDAJkv1wXJTmr5ux0EDvlz5xkUz13ez3YIJ6fmSMpms/edit)

Starting out, the goal is to construct and maintain [a list of ion channels](https://github.com/VahidGh/ChannelWorm/issues/8) relevant to *C. elegans*, and a corresponding list of papers with data plots relevant to each of these ion channels.

Once a collection of such papers is compiled, figures describing the ion channels in question must be extracted as image files.

These image files can then be processed by [digitization software](http://arohatgi.info/WebPlotDigitizer/), which will return datapoints that can be stored in [the project's centralized database](information-management/#data-management) for later retrieval.

## Walkthrough of the process

1. Select a paper and a figure from the list.
    * For example, let's use [figure 2B](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2173050/figure/fig2/) from [this Jospin et al. article](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2173050/).
    * [Here](https://docs.google.com/spreadsheets/d/1jTXDHsLsdK-T_d-RwCb4gmQgMhjumvZE7C_2PEXFYAk/edit#gid=0) is a Google sheet you can choose from
3. Download the image, and crop the relevant portion using image editing software.
    * In our example case we just right-click on the image, save it, and crop out 2B.
      * [The result](https://cloud.githubusercontent.com/assets/7369273/7684968/e5d974c4-fd64-11e4-9cf0-fae6656bc4eb.png)
4. Navigate to the [WebPlotDigitizer](http://arohatgi.info/WebPlotDigitizer/app/?), select "file > load image" and upload the cropped image.
5. Select the "2D (X-Y) Plot" type for I/V curves and the like, and put four points on the axes.
    * Your end result should look [something like this](https://cloud.githubusercontent.com/assets/7369273/7684985/077c3422-fd65-11e4-915e-3cb3e9895f8e.png).
    * Use the arrow keys and the magnifying glass in the upper right to make sure the alignment is accurate.
6. Now enter the values you selected on the axes.
    * In our case, the values [looked like this](https://cloud.githubusercontent.com/assets/7369273/7684983/03f827fc-fd65-11e4-8dc0-f433000a24ed.png)
7. Now add a data point for each data point on the graph.
    * Again, be sure to use the magnifying glass to place the points accurately.
    * Your plot should look something like [this](https://cloud.githubusercontent.com/assets/6655104/6027361/b509831c-abf6-11e4-95a4-372b911533fb.png) by now.
8. Finally, you can click "view data > graph in Plotly" to get something easily sharable with the community.
    * Paste the link to your Plotly graph back into the Google sheet
    * **Tada!**

<div>
    <a href="https://plot.ly/~travs/3/" target="_blank" title="" style="display: block; text-align: center;"><img src="https://plot.ly/~travs/3.png" alt="" style="max-width: 100%;width: 792px;"  width="792" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="travs:3" src="https://plot.ly/embed.js" async></script>
</div>
