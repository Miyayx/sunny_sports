# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_auto_20150412_1003'),
        ('sp', '0008_auto_20150318_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachtrain',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe7\xbc\xb4\xe8\xb4\xb9'), (1, b'\xe5\xb7\xb2\xe7\xbc\xb4\xe8\xb4\xb9')]),
            preserve_default=True,
        ),
    ]
