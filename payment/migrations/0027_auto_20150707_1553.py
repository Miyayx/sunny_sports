# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0026_auto_20150707_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 7, 15, 53, 57, 562183)),
        ),
    ]
