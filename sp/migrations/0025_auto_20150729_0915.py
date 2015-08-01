# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0024_auto_20150728_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='name',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='club',
            name='org_num',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
