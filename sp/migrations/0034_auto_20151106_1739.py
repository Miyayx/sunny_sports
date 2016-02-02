# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0033_auto_20151002_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachproperty',
            name='name',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='studentproperty',
            name='name',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
