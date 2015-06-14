# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0003_train_train_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachorg',
            name='is_active',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
