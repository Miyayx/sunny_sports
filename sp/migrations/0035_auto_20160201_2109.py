# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0034_auto_20151106_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='is_seed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='train',
            name='level',
            field=models.IntegerField(choices=[(1, b'\xe5\x88\x9d\xe7\xba\xa7'), (2, b'\xe4\xb8\xad\xe7\xba\xa7'), (3, b'\xe9\xab\x98\xe7\xba\xa7'), (4, b'\xe8\xbe\x85\xe5\xaf\xbc\xe5\x91\x98\xe7\xa7\x8d\xe5\xad\x90\xe7\x8f\xad')]),
        ),
    ]
