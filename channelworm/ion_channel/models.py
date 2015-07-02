from django.db import models
from django.contrib.auth.models import User


class ParamDict(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class KeyVal(models.Model):
    container = models.ForeignKey(ParamDict, db_index=True)
    key = models.CharField(max_length=240, db_index=True)
    value = models.CharField(max_length=240, db_index=True)

    def __unicode__(self):
        return self.container

Channel_Type_CHOICES = (
    ('Ca', 'Calcium Channel'),
    ('K', 'Potassium Channel')
)
Ion_Type_CHOICES = (
    ('Ca', 'Calcium'),
    ('K', 'Potassium'),
    ('Cl', 'Chloride')
)
Ligand_Type_CHOICES = (

)
class IonChannel(models.Model):
    channel_name = models.CharField(null=True, max_length=300)
    description = models.TextField(blank=True, null=True)
    description_evidences = models.TextField(blank=True, null=True,verbose_name='PMID for description evidence')
    gene_name = models.CharField(blank=True, null=True, max_length=300)
    gene_WB_ID = models.CharField(blank=True, null=True, max_length=300)
    gene_class = models.CharField(blank=True, null=True, max_length=300)
    proteins = models.CharField(blank=True, null=True, max_length=300)
    protein_sequence = models.TextField(blank=True, null=True)
    structure = models.TextField(blank=True, null=True)
    uniprot_ID = models.CharField(blank=True, null=True, max_length=300)
    pdb_ID = models.CharField(blank=True, null=True, max_length=300)
    interpro_ID = models.CharField(blank=True, null=True, max_length=300)
    expression_pattern = models.TextField(blank=True, null=True)
    expression_evidences = models.TextField(blank=True, null=True,verbose_name='PMID for expression evidence')
    channel_type = models.CharField(blank=True, null=True, max_length=300,choices=Channel_Type_CHOICES)
    channel_subtype = models.CharField(blank=True, null=True, max_length=300)
    ion_type = models.CharField(blank=True, null=True, max_length=200,choices=Ion_Type_CHOICES)
    ligand_type = models.CharField(blank=True, null=True, max_length=200,choices=Ligand_Type_CHOICES)
    last_update = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.channel_name


class Cell(models.Model):
    cell_name = models.CharField(max_length=300)
    cell_type = models.CharField(max_length=300,choices=Channel_Type_CHOICES)
    channels = models.ManyToManyField(IonChannel)

    def __unicode__(self):
        return self.cell_name


Reference_Type_CHOICES = (
    ('Genomics', 'Genomics'),
    ('Proteomics', 'Proteomics'),
    ('Electrophysiology', 'Electrophysiology'),
    ('Other', 'Other')
)
class Reference(models.Model):
    doi = models.CharField(max_length=300,unique=True)
    headline = models.TextField(blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    author = models.CharField(max_length=300,blank=True, null=True)
    journal = models.CharField(max_length=300,blank=True, null=True)
    PMID = models.CharField(max_length=300,blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(User,verbose_name='Contributer')
    channels = models.ManyToManyField(IonChannel)
    subject = models.CharField(max_length=300,choices=Reference_Type_CHOICES)
    url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.doi

class Experiment(models.Model):
    reference = models.ForeignKey(Reference)
    create_date = models.DateTimeField(auto_now=True)
    last_update = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(User,verbose_name='Contributer')

    def __unicode__(self):
        return self.reference


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
    protocol_start = models.FloatField(verbose_name='Initial holding potential or stimulated current (V or A)')
    protocol_end = models.FloatField(verbose_name='End of Holding potential or stimulated current (V or A)')
    protocol_step = models.FloatField(verbose_name='Steps of Holding potential or stimulated current (V or A)')
    initial_voltage = models.FloatField(blank=True, null=True, verbose_name='Initial voltage for current-clamp (V)')
    mutants = models.TextField(blank=True, null=True, verbose_name='Additional ion channel mutants (e.g. nf100,n582)')
    blockers = models.TextField(blank=True, null=True, verbose_name='Ion channel blockers (e.g. 500e-6 Cd2+,)')

    def __unicode__(self):
        return self.type + " " + `self.experiment`

# TODO: consider multiple channels

Axis_Type_CHOICES = (
    ('I', 'Current'),
    ('V', 'Voltage'),
    ('T', 'Time'),
    ('G', 'Conductance'),
    ('G/G_max', 'Conductance'),
    ('Po', 'Open Probability'),
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
    figure_ref_caption = models.TextField(verbose_name='Figure caption')
    file = models.ImageField(upload_to='ion_channel/graph/%Y/%m/%d')

    def __unicode__(self):
        return self.experiment+ " " + self.figure_ref_address


class GraphData(models.Model):
    graph = models.ForeignKey(Graph)
    series_name = models.CharField(max_length=200)
    series_data = models.TextField()


Modeling_Method_CHOICES = (
    ('Experimental', 'Experimental'),
    ('Estimated', 'Estimated')
)

Model_Type_CHOICES = (
    ('HH', 'Hodgkin-Huxley'),
    ('Markov', 'Markov')
)
class IonChannelModel(models.Model):
    channel_name = models.ForeignKey(IonChannel)
    model_type = models.CharField(max_length=300,choices=Model_Type_CHOICES, default='HH')
    modeling_type = models.CharField(max_length=300,choices=Modeling_Method_CHOICES,default='Experimental')
    experiment = models.ForeignKey(Experiment)
    graph = models.ForeignKey(Graph)
    username = models.ForeignKey(User,verbose_name='Contributer')
    date = models.DateTimeField(auto_now=True)
    parameters = models.ForeignKey(ParamDict, blank=True, null=True)
    score = models.FloatField(default=None, blank=True, null=True,verbose_name='Evaluated Score')
    neuroML_file = models.FilePathField(blank=True, null=True)
    references = models.ManyToManyField(Reference)

    def __unicode__(self):
        return self.channel_name + " " + self.date
