# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doi', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x_axis_type', models.CharField(max_length=50)),
                ('x_axis_unit', models.CharField(max_length=50)),
                ('y_axis_type', models.CharField(max_length=50)),
                ('y_axis_unit', models.CharField(max_length=50)),
                ('figure_ref_address', models.CharField(max_length=500)),
                ('figure_ref_caption', models.CharField(max_length=100)),
                ('file', models.ImageField(null=True, upload_to=b'')),
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
            name='IonChannelModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('channel_type', models.CharField(max_length=300)),
                ('ion_type', models.CharField(max_length=300)),
                ('expressions', models.CharField(max_length=300)),
                ('experiment', models.ForeignKey(to='ion_channel.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='PatchClamp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=200)),
                ('duration', models.IntegerField()),
                ('delta', models.IntegerField()),
                ('start_time', models.IntegerField()),
                ('end_time', models.IntegerField()),
                ('protocol_start', models.IntegerField()),
                ('protocol_end', models.IntegerField()),
                ('protocol_step', models.IntegerField()),
                ('experiment', models.ForeignKey(to='ion_channel.Experiment')),
            ],
        ),
        migrations.AddField(
            model_name='graph',
            name='experiment',
            field=models.ForeignKey(to='ion_channel.PatchClamp'),
        ),
    ]
