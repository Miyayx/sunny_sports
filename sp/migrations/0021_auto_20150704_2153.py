# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0020_auto_20150704_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.CharField(default=b'', max_length=20, unique=True, serialize=False, primary_key=True),
        ),
    ]
