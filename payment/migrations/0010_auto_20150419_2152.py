# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_auto_20150412_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='comment',
            field=models.CharField(max_length=1000, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='bill_type',
            field=models.IntegerField(default=0, choices=[(0, '\u5feb\u4e50\u4f53\u64cd\u6559\u7ec3\u57f9\u8bad\u8d39\u7528'), (1, '\u5feb\u4e50\u4f53\u64cd\u6bd4\u8d5b\u62a5\u540d\u8d39\u7528')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 20, 13, 52, 38, 888066)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 19, 21, 52, 38, 887993)),
            preserve_default=True,
        ),
    ]
