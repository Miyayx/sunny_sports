# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0032_auto_20150908_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='city',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='train',
            name='dist',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='train',
            name='province',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='train',
            name='address',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
