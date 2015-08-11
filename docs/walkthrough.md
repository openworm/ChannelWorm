Digitization Walkthrough
========================

## Basic figure retrieval and digitization

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
8. Finally, click "view data" and "save", to save your results.
    * **Tada!**

<div>
    <a href="https://plot.ly/~travs/3/" target="_blank" title="" style="display: block; text-align: center;"><img src="https://plot.ly/~travs/3.png" alt="" style="max-width: 100%;width: 792px;"  width="792" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="travs:3" src="https://plot.ly/embed.js" async></script>
</div>

## Calibrating axis offset from the origin

Sometimes the plot you are trying to digitize may have axis that are not centred on the origin, as in this figure:

<img src="http://channelwormdjango-channelworm.rhcloud.com/media/ion_channel/graph/2015/08/09/Screen_Shot_2015-08-09_at_10.56.46_AM.png" width=400px>

In such a case, there are a few approaches you could take. The one we recommend is as follows:

1. Hover over the scale's origin as seen in figure 1 (red arrow) and take note of the real X, Y coordinates (red box).
2. Note the same thing for the two ends of the scale (red circles).
3. Subtract the origin's X component from the extreme X point, to get the real length of scale's X component. Note this value.
4. Do the same for the Y component.
5. Now, with these two lengths we can calibrate the axis. Click the tool icon and start axis calibration. 
6. Now hover over the origin of the actual plot (figure 2) and take note of the coordinates here. 
7. Add the X distance calculated earlier to the X component from the point at the plot's origin. This is where the second X point should be placed.
8. Repeat this for the Y axis.

*Figure 1:*

<img src="../static/calibrate-axis-step-1.png" width=600px>


*Figure 2:*

<img src="../static/calibrate-axis-step-2.png" width=600px>

## Digitizing multiple lines from one figure

In some cases there may be several lines or plots of interest on one set of axes, and thus in the same figure.
In such cases, we would create multiple "datasets" for this figure; one for each line being digitized.

This feature is available under "manage datasets", which is under the tool menu.

**Note:** Be sure to hit "save" on each of the datasets before you close your session, so that each dataset is saved, otherwise they will be lost!

### A special note about I/t plots

In the case of I/t plots, there may be many curves we are interested in, so we want to capture as many as possible.
Since these plots often do not have discrete data points associated with them, do your best to place many points around key features, such as peaks, troughs and steady states. 10-20 points per line should be fine.
Also for I/t plots, please label the datasets according to the held potential.
This may require reading the figure's caption. In the case of figure 3, the caption said that the max voltage was 50mv, and each step was -10mv. This gives datasets for 50, 40, 30 and so on, until the lines can no longer be parsed.

*Figure 3:*

<img src="../static/current-time-plot-1.png" width=600px>
