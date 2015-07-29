# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0028_auto_20150728_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 9, 15, 1, 473730)),
        ),
    ]
