# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0019_auto_20150623_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='submit_status',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe6\x8f\x90\xe4\xba\xa4'), (1, b'\xe5\xb7\xb2\xe6\x8f\x90\xe4\xba\xa4')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.IntegerField(choices=[(0, b'\xe6\x8e\xa5\xe5\x8a\x9b\xe9\x80\x9a\xe5\x85\xb3\xe8\xb5\x9b'), (1, b'\xe7\x94\xb7\xe5\x9b\xa2\xe4\xbd\x93\xe8\xb5\x9b'), (2, b'\xe5\xa5\xb3\xe5\x9b\xa2\xe4\xbd\x93\xe8\xb5\x9b'), (3, b'\xe5\xbf\xab\xe4\xb9\x90\xe9\x9b\x86\xe4\xbd\x93\xe8\x88\x9e')]),
        ),
        migrations.RemoveField(
            model_name='game',
            name='events',
        ),
        migrations.AddField(
            model_name='game',
            name='events',
            field=models.TextField(max_length=20, blank=True),
        ),
    ]
