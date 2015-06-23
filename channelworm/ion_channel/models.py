from django.db import models


class Role(models.Model):
    role = models.CharField(max_length=300,unique=True)
    permissions = models.CharField(max_length=300)

    def __unicode__(self):
        return self.role


class User(models.Model):
    username = models.CharField(max_length=300)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=300)
    role = models.ForeignKey(Role)

    def __unicode__(self):
        return self.username


class Experiment(models.Model):
    doi = models.CharField(max_length=300)

    def __unicode__(self):
        return self.doi


PatchClamp_Type_CHOICES = (
    ('VClamp', 'Voltage-Clamp'),
    ('IClamp', 'Current-Clamp')
)
Patch_Type_CHOICES = (
    ('Whole-cell', 'Whole-cell'),
    ('Single-channel', 'Single-channel')
)

# TODO: Define cell types or get from other table

class PatchClamp(models.Model):
    experiment = models.ForeignKey(Experiment)
    type = models.CharField(max_length=200,choices=PatchClamp_Type_CHOICES)
    patch_type = models.CharField(max_length=200,choices=Patch_Type_CHOICES)
    Ca_concentration = models.FloatField(default=None, blank=True, null=True,verbose_name='The initial molar concentration of Calcium')
    Cl_concentration = models.FloatField(default=None, blank=True, null=True,verbose_name='The initial molar concentration of Chloride')
    cell_type = models.CharField(max_length=200,blank=True,verbose_name='Type of the cell (e.g. muscle, ADAL, Xenopus oocyte)')
    membrane_capacitance = models.FloatField(max_length=200,blank=True, null=True,verbose_name='The capacitance of the membrane (F)')
    cell_age = models.FloatField(default=None, blank=True, null=True,verbose_name='Age of the cell (days)')
    temperature = models.FloatField(default=25, blank=True, null=True,verbose_name='Temperature (Celsius)')
    duration = models.FloatField(verbose_name='Patch-Clamp Duration (s)')
    deltat = models.FloatField(verbose_name='Time interval-Deltat (s)')
    start_time = models.FloatField(verbose_name='Start time (s)')
    end_time = models.FloatField(verbose_name='End time (s)')
    protocol_start = models.FloatField(verbose_name='Beginning of holding potential or stimulated current (V or A)')
    protocol_end = models.FloatField(verbose_name='End of Holding potential or stimulated current (V or A)')
    protocol_step = models.FloatField(verbose_name='Steps of Holding potential or stimulated current (V or A)')
    username = models.ForeignKey(User,verbose_name='Contributer')

    def __unicode__(self):
        return self.type + " " + `self.experiment`


Axis_Type_CHOICES = (
    ('I', 'Current'),
    ('V', 'Voltage'),
    ('T', 'Time'),
    ('G', 'Conductance'),
    ('G/G_max', 'Conductance'),
    ('NP', 'Open Probability'),
    ('Concentration', 'Concentration'),
    ('Bar', 'Bar Chart'),
)

class Graph(models.Model):
    experiment = models.ForeignKey(Experiment, null=True, blank=True)
    patch_clamp = models.ForeignKey(PatchClamp, null=True, blank=True)

    x_axis_type = models.CharField(max_length=50, choices=Axis_Type_CHOICES)
    x_axis_unit = models.CharField(max_length=50,verbose_name='Axis unit in the original figure (e.g. ms)')
    x_axis_toSI = models.FloatField(default=1,verbose_name='Multiply by this value to convert to SI (e.g. 1e-3)')

    y_axis_type = models.CharField(max_length=50, choices=Axis_Type_CHOICES)
    y_axis_unit = models.CharField(max_length=50,verbose_name='Axis unit in the original figure (e.g. mV)')
    y_axis_toSI = models.FloatField(default=1,verbose_name='Multiply by this value to convert to SI (e.g. 1e-3)')


    figure_ref_address = models.CharField(max_length=500,verbose_name='Figure number (e.g. 2A)')
    figure_ref_caption = models.CharField(max_length=500,verbose_name='Figure caption')
    file = models.ImageField(upload_to='ion_channel/graph/%Y/%m/%d')

    def __unicode__(self):
        return self.x_axis_type + "/" + self.y_axis_type+ " " + self.figure_ref_address


class GraphData(models.Model):
    graph = models.ForeignKey(Graph)
    series_name = models.CharField(max_length=200)
    series_data = models.TextField()


Channel_Type_CHOICES = (
    ('Ca', 'Calcium'),
    ('K', 'Potassium')
)
Ion_Type_CHOICES = (
    ('Ca', 'Calcium'),
    ('K', 'Potassium'),
    ('Cl', 'Chloride')
)
class IonChannel(models.Model):
    channel_name = models.CharField(max_length=300)
    channel_type = models.CharField(max_length=300,choices=Channel_Type_CHOICES)
    channel_family = models.CharField(max_length=300)
    ion_type = models.CharField(max_length=200,choices=Ion_Type_CHOICES)

    def __unicode__(self):
        return self.channel_name

class IonChannelModel(models.Model):
    channel_name = models.ForeignKey(IonChannel)
    experiment = models.ForeignKey(Experiment)
    graph = models.ForeignKey(Graph)
    score = models.FloatField(default=None, blank=True, null=True,verbose_name='Evaluated Score')
    username = models.ForeignKey(User,verbose_name='Contributer')
    date = models.DateTimeField(auto_now=True)
    curated = models.BooleanField(default=False)
    neuroML2_file = models.FilePathField()

    def __unicode__(self):
        return self.channel_name + " " + self.date

