# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0028_team_other_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='other_info',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
