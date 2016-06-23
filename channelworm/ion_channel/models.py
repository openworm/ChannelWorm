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
    # references = models.ManyToManyField(Reference)

    def __unicode__(self):
        return self.container.name + "[" + self.key + "=" + self.value + "]"

Channel_Type_CHOICES = (
    ('Calcium Channel', 'Calcium Channel'),
    ('Potassium Channel', 'Potassium Channel'),
    ('Transient Receptor Potential Channel', 'Transient Receptor Potential Channel'),
    ('Cyclic Nucleotide-Gated Channel', 'Cyclic Nucleotide-Gated Channel'),
    ('Ligand-Gated Ion Channel', 'Ligand-Gated Ion Channel'),
    ('Ionotropic Glutamate Receptors', 'Ionotropic Glutamate Receptors'),
    ('DEG/ENaC Channels', 'DEG/ENaC Channels'),
    ('Chloride Channel', 'Chloride Channel')
)
# Channel_Subype_CHOICES = (
#     ('CaV', 'Voltage-gated'),
#     ('KV1', 'Voltage-gated, Shaker/Kv1'),
#     ('KV2', 'Voltage-gated, Shab/Kv2'),
#     ('KV3', 'Voltage-gated, Shaw/Kv3'),
#     ('KV4', 'Voltage-gated, Shal/Kv4'),
#     ('KQT', 'KQT'),
#     ('KV10-12', 'Voltage-gated, Eag-like/Kv10-12'),
#     ('KCa-Slo', 'Calcium-activated Slo'),
#     ('KCa-SK', 'Calcium-activated SK'),
#     ('TWK', 'TWK'),
#     ('Kir', 'Inward-Rectifier'),
#     ('Cation, TRP', 'Transient Receptor Potential Cation Channel'),
#     ('CNG', 'Cyclic Nucleotide-Gated Channel'),
#     ('LGIC', 'Ligand-Gated Ion Channel'),
#     ('iGluRs', 'Ionotropic Glutamate Receptors'),
#     ('DEG/ENaC/ASIC', 'DEGenerin/Epithelial Na+ Channels/Acid Sensing Ion Channels'),
#     ('CLC', 'Chloride Channels And Transporters'),
#     ('Auxiliary', 'Auxiliary subunit')
# )
Ion_Type_CHOICES = (
    ('Ca2+', 'Calcium'),
    ('K+', 'Potassium'),
    ('Cl-', 'Chloride'),
    ('Na+', 'Cation'),
    ('Cation', 'Cation')
)
Ligand_Type_CHOICES = (
    ('ATP', 'ATP'),
    ('Glutamate', 'Glutamate'),
    ('Acetylcholine', 'Acetylcholine'),
    ('Serotonin', 'Serotonin'),
    ('Tyramine', 'Tyramine')
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
    expression_pattern = models.TextField(blank=True, null=True)
    expression_evidences = models.TextField(blank=True, null=True,verbose_name='PMID for expression evidence')
    last_update = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.channel_name

# TODO: Get cells from PyOW

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
    ion_channels = models.ManyToManyField(IonChannel,blank=True)
    membrane_capacitance = models.FloatField(max_length=200,blank=True, null=True,verbose_name='Capacitance of the membrane (F)')
    specific_capacitance = models.FloatField(default=0.01,blank=True, null=True,verbose_name='Specific capacitance of the membrane (F/m2)')
    area = models.FloatField(default=6e-9, blank=True, null=True,verbose_name='Total area of the cell (m2)')

    def __unicode__(self):
        return self.cell_type + ", " + self.cell_name
#
# class CellChannel(models.Model):
#     cell = models.ForeignKey(Cell)
#     ion_channel = models.ForeignKey(IonChannel)
#     channel_density = models.FloatField(blank=True, null=True,verbose_name='Density of the channel in cell (1/m2)')
#     e_rev = models.FloatField(blank=True, null=True,verbose_name='Reversal potential of the channel in cell (V)')
#     reference = models.ManyToManyField(Reference)
#
#     def __unicode__(self):
#         return `self.cell` + ", " + `self.ion_channel`

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
    username = models.ForeignKey(User,verbose_name='Contributor')
    ion_channels = models.ManyToManyField(IonChannel,blank=True)
    cells = models.ManyToManyField(Cell,blank=True)
    subject = models.CharField(max_length=300,choices=Reference_Type_CHOICES)
    file_url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.doi + ": " + self.citation + ", " + self.year


class CellChannel(models.Model):
    cell = models.ForeignKey(Cell)
    ion_channel = models.ForeignKey(IonChannel)
    channel_density = models.FloatField(blank=True, null=True,verbose_name='Density of the channel in cell (1/m2)')
    reference = models.ForeignKey(Reference)

    def __unicode__(self):
        return repr(self.cell) + ", " + repr(self.ion_channel)


# TODO: Separate experiment conditions from patch clamp

class Experiment(models.Model):
    reference = models.ForeignKey(Reference)
    create_date = models.DateTimeField()
    last_update = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(User,verbose_name='Contributer')
    comments = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.reference.doi + ": " + self.reference.citation + ", " + self.reference.year


PatchClamp_Type_CHOICES = (
    ('VClamp', 'Voltage-Clamp'),
    ('IClamp', 'Current-Clamp')
)
Patch_Type_CHOICES = (
    ('Whole-cell', 'Whole-cell'),
    ('Single-channel', 'Single-channel')
)

# TODO: Consider measurement fields: https://pypi.python.org/pypi/django-measurement

class PatchClamp(models.Model):
    experiment = models.ForeignKey(Experiment)
    ion_channel = models.ForeignKey(IonChannel)
    type = models.CharField(max_length=200,choices=PatchClamp_Type_CHOICES)
    patch_type = models.CharField(max_length=200,choices=Patch_Type_CHOICES)
    cell = models.ForeignKey(Cell, blank=True, null=True,verbose_name='Type of the cell (e.g. muscle, ADAL, Xenopus Oocyte)')
    duration = models.FloatField(verbose_name='Patch-Clamp Duration (ms)')
    deltat = models.FloatField(default=0.01, verbose_name='Time interval-Deltat (ms)')
    start_time = models.FloatField(default=0,verbose_name='Start time (ms)')
    end_time = models.FloatField(verbose_name='End time (ms) (default=duration)')
    protocol_start = models.FloatField(verbose_name='Initial holding potential or stimulated current (mV or pA)')
    protocol_end = models.FloatField(verbose_name='End of Holding potential or stimulated current (mV or pA)')
    protocol_step = models.FloatField(verbose_name='Steps of Holding potential or stimulated current (mV or pA)')
    cell_age = models.FloatField(default=None, blank=True, null=True,verbose_name='Age of the cell (days)')
    membrane_capacitance = models.FloatField(max_length=200,blank=True, null=True,verbose_name='Capacitance of the membrane (F)')
    temperature = models.FloatField(default=21, blank=True, null=True,verbose_name='Temperature (Celsius)')
    initial_voltage = models.FloatField(blank=True, null=True, verbose_name='Initial holding potential (mV)')
    Ca_concentration = models.FloatField(default=None, blank=True, null=True,verbose_name='Initial molar concentration of Calcium (uM)')
    Cl_concentration = models.FloatField(default=None, blank=True, null=True,verbose_name='Initial molar concentration of Chloride (mM)')
    mutants = models.CharField(max_length=300, blank=True, null=True, verbose_name='Additional ion channel mutants (e.g. nf100,n582,...)')
    blockers = models.CharField(max_length=300, blank=True, null=True, verbose_name='Ion channel blockers (e.g. 500e-6 Cd2+,...)')
    extra_solution = models.TextField(blank=True, null=True, verbose_name='Extracellular Solution (e.g. 140e-3 NaCl, 5e-3 KCl,...)')
    pipette_solution = models.TextField(blank=True, null=True, verbose_name='Pipette Solution (e.g. 120e-3 KCl, 20e-3 KOH,...)')

    def __unicode__(self):
        return repr(self.ion_channel) + " " + repr(self.experiment) + " " + self.type


# TODO: consider multiple channels

Axis_Type_CHOICES = (
    ('I', 'Current'),
    ('I_ss', 'Steady-state Current'),
    ('I_peak', 'Peak Current'),
    ('I_norm', 'Normalized Current'),
    ('V', 'Voltage'),
    ('T', 'Time'),
    ('G', 'Conductance'),
    ('G/G_max', 'G/G_max'),
    ('Po', 'Open Probability'),
    ('Po_Peak', 'Peak Open Probability'),
    ('Ca_concentration', 'Calcium Concentration'),
    ('Cl_concentration', 'Chloride Concentration'),
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

    ion_channel = models.ManyToManyField(IonChannel)
    mutants = models.CharField(max_length=300, blank=True, null=True, verbose_name='Additional ion channel mutants (e.g. nf100,n582)')

    figure_ref_address = models.CharField(max_length=50,verbose_name='Figure number (e.g. 2A)')
    figure_ref_caption = models.TextField(verbose_name='Figure caption')
    file = models.ImageField(upload_to='ion_channel/graph/%Y/%m/%d')

    def __unicode__(self):
        return str(self.y_axis_type) + "/" + str(self.x_axis_type) + " relation, Fig. " + \
               str(self.figure_ref_address) + ", From:  " + self.experiment.reference.citation + \
               ", " + self.experiment.reference.year


class GraphData(models.Model):
    graph = models.ForeignKey(Graph)
    series_name = models.CharField(max_length=200)
    series_data = models.TextField()

    def __unicode__(self):
        return self.series_name

    def asarray(self):
        xy = self.series_data.splitlines()
        data = list()
        for row in xy:
            data += [map(float, row.split(','))]

        return data


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
    cell_name = models.ForeignKey(Cell, blank=True, null=True)
    model_type = models.CharField(max_length=300,choices=Model_Type_CHOICES, default='HH')
    modeling_type = models.CharField(max_length=300,choices=Modeling_Method_CHOICES,default='Experimental')
    experiment = models.ForeignKey(Experiment)
    graphs = models.ManyToManyField(Graph)
    username = models.ManyToManyField(User,verbose_name='Curator(s)')
    date = models.DateTimeField(auto_now=True)
    parameters = models.ManyToManyField(ParamDict)
    score = models.FloatField(default=None, blank=True, null=True,verbose_name='Evaluated Score')
    neuroML_file = models.FilePathField(blank=True, null=True)
    references = models.ManyToManyField(Reference)

    def __unicode__(self):
        return repr(self.channel_name) + " " + repr(self.experiment)

class Protein(models.Model):
    name = models.CharField(max_length=300, unique=True)
    ion_channel = models.ForeignKey(IonChannel)
    sequence = models.TextField(blank=True, null=True)
    fasta = models.TextField(blank=True, null=True)
    gi = models.CharField(max_length=300,blank=True, null=True,verbose_name='GI number')
    uniprot_ID = models.CharField(blank=True, null=True, max_length=300)
    wb_ID = models.CharField(blank=True, null=True, max_length=300)
    pdb_ID = models.CharField(blank=True, null=True, max_length=300)
    interpro_ID = models.CharField(blank=True, null=True, max_length=300)
    structure = models.TextField(blank=True, null=True)
    structure_image = models.ImageField(blank=True, null=True, upload_to='ion_channel/structures/')

    def __unicode__(self):
        return self.name
