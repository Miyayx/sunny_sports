# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0035_auto_20160201_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='student_money',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='train',
            name='level',
            field=models.IntegerField(choices=[(0, b'\xe8\xbe\x85\xe5\xaf\xbc\xe5\x91\x98\xe5\x9f\xb9\xe8\xae\xad\xe7\x8f\xad'), (1, b'\xe5\x88\x9d\xe7\xba\xa7'), (2, b'\xe4\xb8\xad\xe7\xba\xa7'), (3, b'\xe9\xab\x98\xe7\xba\xa7')]),
        ),
    ]
