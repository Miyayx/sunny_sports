# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0017_auto_20150502_2222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='expire_date',
        ),
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 2, 22, 23, 38, 405034)),
            preserve_default=True,
        ),
    ]
