# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ion_channel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Protein',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=300)),
                ('sequence', models.TextField(null=True, blank=True)),
                ('fasta', models.TextField(null=True, blank=True)),
                ('gi', models.CharField(max_length=300, null=True, verbose_name=b'GI number', blank=True)),
                ('uniprot_ID', models.CharField(max_length=300, null=True, blank=True)),
                ('wb_ID', models.CharField(max_length=300, null=True, blank=True)),
                ('pdb_ID', models.CharField(max_length=300, null=True, blank=True)),
                ('interpro_ID', models.CharField(max_length=300, null=True, blank=True)),
                ('structure', models.TextField(null=True, blank=True)),
                ('structure_image', models.ImageField(null=True, upload_to=b'ion_channel/structures/', blank=True)),
            ],
        ),
        migrations.RenameField(
            model_name='ionchannelmodel',
            old_name='graph',
            new_name='main_graph',
        ),
        migrations.RemoveField(
            model_name='ionchannel',
            name='interpro_ID',
        ),
        migrations.RemoveField(
            model_name='ionchannel',
            name='pdb_ID',
        ),
        migrations.RemoveField(
            model_name='ionchannel',
            name='protein_sequence',
        ),
        migrations.RemoveField(
            model_name='ionchannel',
            name='structure',
        ),
        migrations.RemoveField(
            model_name='ionchannel',
            name='structure_image',
        ),
        migrations.RemoveField(
            model_name='ionchannel',
            name='uniprot_ID',
        ),
        migrations.AddField(
            model_name='ionchannelmodel',
            name='cell_name',
            field=models.ForeignKey(blank=True, to='ion_channel.Cell', null=True),
        ),
        migrations.RemoveField(
            model_name='ionchannelmodel',
            name='username',
        ),
        migrations.AddField(
            model_name='ionchannelmodel',
            name='username',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'Curator(s)'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='username',
            field=models.ForeignKey(verbose_name=b'Contributor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='protein',
            name='ion_channel',
            field=models.ForeignKey(to='ion_channel.IonChannel'),
        ),
    ]
