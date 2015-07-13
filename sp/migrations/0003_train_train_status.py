# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0002_remove_train_train_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='train_status',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe5\xbc\x80\xe5\xa7\x8b'), (1, b'\xe8\xbf\x9b\xe8\xa1\x8c\xe4\xb8\xad'), (2, b'\xe7\xbb\x93\xe6\x9d\x9f')]),
            preserve_default=True,
        ),
    ]
