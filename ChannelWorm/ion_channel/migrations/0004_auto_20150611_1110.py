# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ion_channel', '0003_auto_20150605_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='experiment',
            field=models.ForeignKey(blank=True, to='ion_channel.Experiment', null=True),
        ),
        migrations.AlterField(
            model_name='graph',
            name='patch_clamp',
            field=models.ForeignKey(blank=True, to='ion_channel.PatchClamp', null=True),
        ),
    ]
