# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0030_auto_20150815_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='no',
            field=models.CharField(max_length=100, serialize=False, primary_key=True),
        ),
    ]
