# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0023_auto_20150707_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='total_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='teamevent',
            name='award',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x9a\x82\xe6\x97\xa0\xe7\xbb\x93\xe6\x9e\x9c'), (1, b'\xe4\xb8\x80\xe7\xad\x89\xe5\xa5\x96'), (2, b'\xe4\xba\x8c\xe7\xad\x89\xe5\xa5\x96'), (3, b'\xe4\xb8\x89\xe7\xad\x89\xe5\xa5\x96'), (4, b'\xe7\xbc\xba\xe8\xb5\x9b')]),
        ),
    ]
