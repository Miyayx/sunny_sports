# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0007_auto_20150314_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coachproperty',
            name='age',
        ),
        migrations.RemoveField(
            model_name='judgeproperty',
            name='age',
        ),
        migrations.RemoveField(
            model_name='studentproperty',
            name='age',
        ),
        migrations.AlterField(
            model_name='train',
            name='train_etime',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='train',
            name='train_stime',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
