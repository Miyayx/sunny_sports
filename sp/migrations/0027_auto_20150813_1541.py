# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0026_auto_20150801_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachorg',
            name='org_num',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='coachorg',
            name='shortname',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='gameorg',
            name='org_num',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='gameorg',
            name='shortname',
            field=models.CharField(max_length=30),
        ),
    ]
