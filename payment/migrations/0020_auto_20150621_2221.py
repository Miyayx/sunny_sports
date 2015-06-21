# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0019_auto_20150621_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 21, 22, 21, 20, 175651)),
        ),
    ]
