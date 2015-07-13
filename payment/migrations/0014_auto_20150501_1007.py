# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0013_auto_20150501_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 2, 2, 7, 32, 365801)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 1, 10, 7, 32, 365739)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='trade_status',
            field=models.CharField(default=b'INIT', max_length=50),
            preserve_default=True,
        ),
    ]
