# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_auto_20150419_2152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='comment',
            new_name='body',
        ),
        migrations.AlterField(
            model_name='bill',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 20, 13, 59, 41, 662439)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 19, 21, 59, 41, 662339)),
            preserve_default=True,
        ),
    ]
