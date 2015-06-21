# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0018_auto_20150502_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 21, 22, 14, 39, 247897)),
        ),
    ]
