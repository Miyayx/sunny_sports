# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_auto_20150411_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 7, 24, 5, 722248)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 11, 15, 24, 5, 722186)),
            preserve_default=True,
        ),
    ]
