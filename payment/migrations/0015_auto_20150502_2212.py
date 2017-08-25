# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0014_auto_20150501_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 3, 14, 11, 35, 429859)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 2, 22, 11, 35, 429799)),
            preserve_default=True,
        ),
    ]
