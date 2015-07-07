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
    channel_type = models.CharField(blank=True, null=True, max_length=300,choices=Channel_Type_CHOICES)
    channel_subtype = models.CharField(blank=True, null=True, max_length=300)
    ion_type = models.CharField(blank=True, null=True, max_length=200,choices=Ion_Type_CHOICES)
    ligand_type = models.CharField(blank=True, null=True, max_length=200,choices=Ligand_Type_CHOICES)
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
    last_update = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.channel_name

Cell_Type_CHOICES = (
    ('Muscle', 'Muscle'),
    ('Neuron', 'Neuron'),
    ('Motor Neuron', 'Motor Neuron'),
    ('Xenopus Oocyte', 'Xenopus Oocyte'),
    ('Generic', 'Generic'),
)
class Cell(models.Model):
    cell_name = models.CharField(max_length=300,unique=True,default='Generic')
    cell_type = models.CharField(max_length=300,choices=Cell_Type_CHOICES,default='Generic')
    ion_channels = models.ManyToManyField(IonChannel,blank=True, null=True)
    membrane_capacitance = models.FloatField(max_length=200,blank=True, null=True,verbose_name='Capacitance of the membrane (F)')
    specific_capacitance = models.FloatField(default=0.01,blank=True, null=True,verbose_name='Specific capacitance of the membrane (F/m2)')
    area = models.FloatField(default=6e-9, blank=True, null=True,verbose_name='Total area of the cell (m2)')

    def __unicode__(self):
        return self.cell_type + " " + self.cell_name

Reference_Type_CHOICES = (
    ('Genomics', 'Genomics'),
    ('Proteomics', 'Proteomics'),
    ('Electrophysiology', 'Electrophysiology'),
    ('Other', 'Other')
)
class Reference(models.Model):
    doi = models.CharField(max_length=300,unique=True)
    PMID = models.CharField(max_length=300,blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    citation = models.TextField(blank=True, null=True)
    year = models.CharField(max_length=300,blank=True, null=True)
    authors = models.CharField(max_length=300,blank=True, null=True)
    journal = models.CharField(max_length=300,blank=True, null=True)
    volume = models.CharField(max_length=300,blank=True, null=True)
    issue = models.CharField(max_length=300,blank=True, null=True)
    pages = models.CharField(max_length=300,blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(User,verbose_name='Contributer')
    ion_channels = models.ManyToManyField(IonChannel,blank=True, null=True)
    cells = models.ManyToManyField(Cell,blank=True, null=True)
    subject = models.CharField(max_length=300,choices=Reference_Type_CHOICES)
    file_url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.doi


class CellChannel(models.Model):
    cell = models.ForeignKey(Cell)
    ion_channel = models.ForeignKey(IonChannel)
    channel_density = models.FloatField(blank=True, null=True,verbose_name='Density of the channel in cell (1/m2)')
    reference = models.ForeignKey(Reference)

    def __unicode__(self):
        return `self.cell` + " " + `self.ion_channel`


class Experiment(models.Model):
    reference = models.ForeignKey(Reference)
    create_date = models.DateTimeField(auto_now=True)
    last_update = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(User,verbose_name='Contributer')
    comments = models.TextField(blank=True, null=True,)

    def __unicode__(self):
        return `self.reference` + " " + self.reference.title


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
    ion_channel = models.ForeignKey(IonChannel)
    type = models.CharField(max_length=200,choices=PatchClamp_Type_CHOICES)
    patch_type = models.CharField(max_length=200,choices=Patch_Type_CHOICES)
    cell = models.ForeignKey(Cell, blank=True, null=True,verbose_name='Type of the cell (e.g. muscle, ADAL, Xenopus oocyte)')
    duration = models.FloatField(verbose_name='Patch-Clamp Duration (s)')
    deltat = models.FloatField(verbose_name='Time interval-Deltat (s)')
    start_time = models.FloatField(verbose_name='Start time (s)')
    end_time = models.FloatField(verbose_name='End time (s)')
    protocol_start = models.FloatField(verbose_name='Initial holding potential or stimulated current (V or A)')
    protocol_end = models.FloatField(verbose_name='End of Holding potential or stimulated current (V or A)')
    protocol_step = models.FloatField(verbose_name='Steps of Holding potential or stimulated current (V or A)')
    cell_age = models.FloatField(default=None, blank=True, null=True,verbose_name='Age of the cell (days)')
    membrane_capacitance = models.FloatField(max_length=200,blank=True, null=True,verbose_name='Capacitance of the membrane (F)')
    temperature = models.FloatField(default=25, blank=True, null=True,verbose_name='Temperature (Celsius)')
    initial_voltage = models.FloatField(blank=True, null=True, verbose_name='Initial voltage for current-clamp (V)')
    Ca_concentration = models.FloatField(default=None, blank=True, null=True,verbose_name='Initial molar concentration of Calcium')
    Cl_concentration = models.FloatField(default=None, blank=True, null=True,verbose_name='Initial molar concentration of Chloride')
    mutants = models.TextField(blank=True, null=True, verbose_name='Additional ion channel mutants (e.g. nf100,n582)')
    blockers = models.TextField(blank=True, null=True, verbose_name='Ion channel blockers (e.g. 500e-6 Cd2+,)')

    def __unicode__(self):
        return `self.ion_channel` + " " + `self.experiment` + " " + self.type

# TODO: consider multiple channels

Axis_Type_CHOICES = (
    ('I', 'Current'),
    ('I_ss', 'Steady-state Current'),
    ('I_peak', 'Peak Current'),
    ('V', 'Voltage'),
    ('T', 'Time'),
    ('G', 'Conductance'),
    ('G/G_max', 'G/G_max'),
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
        return `self.experiment`+ " " + self.figure_ref_address


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
        return `self.channel_name` + " " + `self.experiment`
