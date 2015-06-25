# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cell_name', models.CharField(max_length=300)),
                ('cell_type', models.CharField(max_length=300, choices=[(b'Ca', b'Calcium Channel'), (b'K', b'Potassium Channel')])),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x_axis_type', models.CharField(max_length=50, choices=[(b'I', b'Current'), (b'V', b'Voltage'), (b'T', b'Time'), (b'G', b'Conductance'), (b'G/G_max', b'Conductance'), (b'NP', b'Open Probability'), (b'Concentration', b'Concentration'), (b'Bar', b'Bar Chart')])),
                ('x_axis_unit', models.CharField(max_length=50, verbose_name=b'Axis unit in the original figure (e.g. ms)')),
                ('x_axis_toSI', models.FloatField(default=1, verbose_name=b'Multiply by this value to convert to SI (e.g. 1e-3)')),
                ('y_axis_type', models.CharField(max_length=50, choices=[(b'I', b'Current'), (b'V', b'Voltage'), (b'T', b'Time'), (b'G', b'Conductance'), (b'G/G_max', b'Conductance'), (b'NP', b'Open Probability'), (b'Concentration', b'Concentration'), (b'Bar', b'Bar Chart')])),
                ('y_axis_unit', models.CharField(max_length=50, verbose_name=b'Axis unit in the original figure (e.g. mV)')),
                ('y_axis_toSI', models.FloatField(default=1, verbose_name=b'Multiply by this value to convert to SI (e.g. 1e-3)')),
                ('figure_ref_address', models.CharField(max_length=500, verbose_name=b'Figure number (e.g. 2A)')),
                ('figure_ref_caption', models.TextField(verbose_name=b'Figure caption')),
                ('file', models.ImageField(upload_to=b'ion_channel/graph/%Y/%m/%d')),
                ('experiment', models.ForeignKey(blank=True, to='ion_channel.Experiment', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GraphData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('series_name', models.CharField(max_length=200)),
                ('series_data', models.TextField()),
                ('graph', models.ForeignKey(to='ion_channel.Graph')),
            ],
        ),
        migrations.CreateModel(
            name='IonChannel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('channel_name', models.CharField(max_length=300, null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('description_evidences', models.TextField(null=True, verbose_name=b'PMID for description evidence', blank=True)),
                ('protein_short_name', models.CharField(max_length=300, null=True, blank=True)),
                ('proteins', models.CharField(max_length=300, null=True, blank=True)),
                ('gene_WB_ID', models.CharField(max_length=300, null=True, blank=True)),
                ('gene_class', models.CharField(max_length=300, null=True, blank=True)),
                ('expression_pattern', models.TextField(null=True, blank=True)),
                ('expression_evidences', models.TextField(null=True, verbose_name=b'PMID for expression evidence', blank=True)),
                ('channel_type', models.CharField(blank=True, max_length=300, null=True, choices=[(b'Ca', b'Calcium Channel'), (b'K', b'Potassium Channel')])),
                ('channel_subtype', models.CharField(max_length=300, null=True, blank=True)),
                ('ion_type', models.CharField(blank=True, max_length=200, null=True, choices=[(b'Ca', b'Calcium'), (b'K', b'Potassium'), (b'Cl', b'Chloride')])),
            ],
        ),
        migrations.CreateModel(
            name='IonChannelModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_type', models.CharField(max_length=300, choices=[(b'Experimental', b'Experimental'), (b'Estimated', b'Estimated')])),
                ('score', models.FloatField(default=None, null=True, verbose_name=b'Evaluated Score', blank=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('neuroML_file', models.FilePathField()),
                ('channel_name', models.ForeignKey(to='ion_channel.IonChannel')),
                ('experiment', models.ForeignKey(to='ion_channel.Experiment')),
                ('graph', models.ForeignKey(to='ion_channel.Graph')),
            ],
        ),
        migrations.CreateModel(
            name='PatchClamp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=200, choices=[(b'VClamp', b'Voltage-Clamp'), (b'IClamp', b'Current-Clamp')])),
                ('patch_type', models.CharField(max_length=200, choices=[(b'Whole-cell', b'Whole-cell'), (b'Single-channel', b'Single-channel')])),
                ('Ca_concentration', models.FloatField(default=None, null=True, verbose_name=b'The initial molar concentration of Calcium', blank=True)),
                ('Cl_concentration', models.FloatField(default=None, null=True, verbose_name=b'The initial molar concentration of Chloride', blank=True)),
                ('cell_type', models.CharField(max_length=200, verbose_name=b'Type of the cell (e.g. muscle, ADAL, Xenopus oocyte)', blank=True)),
                ('membrane_capacitance', models.FloatField(max_length=200, null=True, verbose_name=b'The capacitance of the membrane (F)', blank=True)),
                ('cell_age', models.FloatField(default=None, null=True, verbose_name=b'Age of the cell (days)', blank=True)),
                ('temperature', models.FloatField(default=25, null=True, verbose_name=b'Temperature (Celsius)', blank=True)),
                ('duration', models.FloatField(verbose_name=b'Patch-Clamp Duration (s)')),
                ('deltat', models.FloatField(verbose_name=b'Time interval-Deltat (s)')),
                ('start_time', models.FloatField(verbose_name=b'Start time (s)')),
                ('end_time', models.FloatField(verbose_name=b'End time (s)')),
                ('protocol_start', models.FloatField(verbose_name=b'Initial holding potential or stimulated current (V or A)')),
                ('protocol_end', models.FloatField(verbose_name=b'End of Holding potential or stimulated current (V or A)')),
                ('protocol_step', models.FloatField(verbose_name=b'Steps of Holding potential or stimulated current (V or A)')),
                ('initial_voltage', models.FloatField(null=True, verbose_name=b'Initial voltage for current-clamp (V)', blank=True)),
                ('mutants', models.TextField(null=True, verbose_name=b'Additional ion channel mutants (e.g. nf100,n582)', blank=True)),
                ('blockers', models.TextField(null=True, verbose_name=b'Ion channel blockers (e.g. 500e-6 Cd2+,)', blank=True)),
                ('experiment', models.ForeignKey(to='ion_channel.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doi', models.CharField(unique=True, max_length=300)),
                ('headline', models.TextField(null=True, blank=True)),
                ('publish_date', models.DateTimeField(null=True, blank=True)),
                ('author', models.CharField(max_length=300, null=True, blank=True)),
                ('PMID', models.CharField(max_length=300, null=True, blank=True)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=300, choices=[(b'Genomics', b'Genomics'), (b'Proteomics', b'Proteomics'), (b'Electrophysiology', b'Electrophysiology'), (b'Other', b'Other')])),
                ('file_path', models.FilePathField(null=True, blank=True)),
                ('channels', models.ManyToManyField(to='ion_channel.IonChannel')),
                ('username', models.ForeignKey(verbose_name=b'Contributer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ionchannelmodel',
            name='references',
            field=models.ManyToManyField(to='ion_channel.Reference'),
        ),
        migrations.AddField(
            model_name='ionchannelmodel',
            name='username',
            field=models.ForeignKey(verbose_name=b'Contributer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='graph',
            name='patch_clamp',
            field=models.ForeignKey(blank=True, to='ion_channel.PatchClamp', null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='reference',
            field=models.ForeignKey(to='ion_channel.Reference'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='username',
            field=models.ForeignKey(verbose_name=b'Contributer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cell',
            name='channels',
            field=models.ManyToManyField(to='ion_channel.IonChannel'),
        ),
    ]
