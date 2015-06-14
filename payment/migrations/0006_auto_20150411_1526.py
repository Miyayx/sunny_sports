# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_auto_20150411_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='id',
        ),
        migrations.AlterField(
            model_name='bill',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 7, 26, 17, 669948)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='no',
            field=models.CharField(max_length=36, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 11, 15, 26, 17, 669888)),
            preserve_default=True,
        ),
    ]
