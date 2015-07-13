# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='no',
            field=models.CharField(default=b'', max_length=36),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 6, 49, 38, 256414)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 11, 14, 49, 38, 256355)),
            preserve_default=True,
        ),
    ]
