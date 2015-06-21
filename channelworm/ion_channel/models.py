from django.db import models

# Create your models here.

class Experiment(models.Model):
    doi = models.CharField(max_length=300)

    def __unicode__(self):
        return self.doi


class IonChannelModel(models.Model):
    experiment = models.ForeignKey(Experiment)
    channel_type = models.CharField(max_length=300)
    ion_type = models.CharField(max_length=300)
    expressions = models.CharField(max_length=300)

    def __unicode__(self):
        return self.channel_type + self.ion_type


PatchClamp_Type_CHOICES = (
    ('VClamp', 'Voltage-Clamp'),
    ('IClamp', 'Current-Clamp')
)

class PatchClamp(models.Model):
    experiment = models.ForeignKey(Experiment)
    type = models.CharField(max_length=200,choices=PatchClamp_Type_CHOICES)
    duration = models.FloatField(verbose_name='Patch-Clamp Duration (s)')
    deltat = models.FloatField(verbose_name='Time interval-Deltat (s)')
    start_time = models.FloatField(verbose_name='Start time (s)')
    end_time = models.FloatField(verbose_name='End time (s)')
    protocol_start = models.FloatField(verbose_name='Beginning of holding potential or stimulated current (V or A)')
    protocol_end = models.FloatField(verbose_name='End of Holding potential or stimulated current (V or A)')
    protocol_step = models.FloatField('Steps of Holding potential or stimulated current (V or A)')

    def __unicode__(self):
        return self.type + " " + `self.duration`


class Graph(models.Model):
    experiment = models.ForeignKey(Experiment, null=True, blank=True)
    patch_clamp = models.ForeignKey(PatchClamp, null=True, blank=True)

    x_axis_type = models.CharField(max_length=50)
    x_axis_unit = models.CharField(max_length=50)

    y_axis_type = models.CharField(max_length=50)
    y_axis_unit = models.CharField(max_length=50)

    figure_ref_address = models.CharField(max_length=500)
    figure_ref_caption = models.CharField(max_length=100)
    file = models.ImageField(upload_to='ion_channel/graph/%Y/%m/%d')

    def __unicode__(self):
        return self.x_axis_type + " " + self.x_axis_unit


class GraphData(models.Model):
    graph = models.ForeignKey(Graph)
    series_name = models.CharField(max_length=200)
    series_data = models.TextField()
