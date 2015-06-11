# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ion_channel', '0002_auto_20150605_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='file',
            field=models.ImageField(default=datetime.datetime(2015, 6, 5, 9, 8, 9, 538271, tzinfo=utc), upload_to=b'ion_channel/graph/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]
