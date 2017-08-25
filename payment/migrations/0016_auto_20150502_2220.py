# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0015_auto_20150502_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 3, 14, 20, 15, 822334)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 2, 22, 20, 15, 822266)),
            preserve_default=True,
        ),
    ]
