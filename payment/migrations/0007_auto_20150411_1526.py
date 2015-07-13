# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_auto_20150411_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 7, 26, 28, 323215)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 11, 15, 26, 28, 323131)),
            preserve_default=True,
        ),
    ]
