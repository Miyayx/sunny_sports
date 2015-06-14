# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0009_auto_20150412_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachorg',
            name='ali_email',
            field=models.EmailField(max_length=75, null=True),
            preserve_default=True,
        ),
    ]
