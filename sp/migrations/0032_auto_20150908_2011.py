# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0031_auto_20150829_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachproperty',
            name='id_type',
            field=models.IntegerField(default=0, choices=[(0, b'\xe8\xba\xab\xe4\xbb\xbd\xe8\xaf\x81\xe5\x8f\xb7'), (1, b'\xe6\x8a\xa4\xe7\x85\xa7\xe5\x8f\xb7\xe7\xa0\x81')]),
        ),
        migrations.AddField(
            model_name='studentproperty',
            name='id_type',
            field=models.IntegerField(default=0, choices=[(0, b'\xe8\xba\xab\xe4\xbb\xbd\xe8\xaf\x81\xe5\x8f\xb7'), (1, b'\xe6\x8a\xa4\xe7\x85\xa7\xe5\x8f\xb7\xe7\xa0\x81')]),
        ),
        migrations.AlterField(
            model_name='coachproperty',
            name='identity',
            field=models.CharField(max_length=30, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentproperty',
            name='identity',
            field=models.CharField(max_length=30, unique=True, null=True),
        ),
    ]
