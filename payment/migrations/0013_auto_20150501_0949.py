# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_auto_20150430_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='trade_status',
            field=models.CharField(default=b'INIT', max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 2, 1, 49, 15, 708936)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 1, 9, 49, 15, 708873)),
            preserve_default=True,
        ),
    ]
