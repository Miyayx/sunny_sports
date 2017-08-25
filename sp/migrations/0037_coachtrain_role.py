# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0036_auto_20160602_0657'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachtrain',
            name='role',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x99\xae\xe9\x80\x9a'), (1, b'\xe5\xad\xa6\xe7\x94\x9f')]),
        ),
    ]
