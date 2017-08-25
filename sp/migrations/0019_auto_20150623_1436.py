# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0018_gameorg'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='org',
            field=models.ForeignKey(default=None, to='sp.GameOrg'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.IntegerField(unique=True, serialize=False, primary_key=True, choices=[(0, b'centre'), (1, b'coach_org'), (2, b'student'), (3, b'coach'), (4, b'club'), (5, b'group'), (6, b'committee'), (7, b'game_org')]),
        ),
    ]
