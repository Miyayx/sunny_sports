# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0011_auto_20150419_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='judge',
            name='club',
        ),
        migrations.RemoveField(
            model_name='judge',
            name='property',
        ),
        migrations.DeleteModel(
            name='Judge',
        ),
        migrations.RemoveField(
            model_name='judgeproperty',
            name='user',
        ),
        migrations.DeleteModel(
            name='JudgeProperty',
        ),
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.IntegerField(unique=True, serialize=False, primary_key=True, choices=[(0, b'centre'), (1, b'coach_org'), (2, b'student'), (3, b'coach'), (4, b'club'), (5, b'team'), (6, b'committee')]),
            preserve_default=True,
        ),
    ]
