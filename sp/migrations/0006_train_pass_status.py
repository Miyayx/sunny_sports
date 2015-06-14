# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0005_auto_20150314_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='pass_status',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe5\xae\xa1\xe6\xa0\xb8'), (1, b'\xe5\xae\xa1\xe6\xa0\xb8\xe4\xb8\xad'), (2, b'\xe5\xae\xa1\xe6\xa0\xb8\xe6\x9c\xaa\xe9\x80\x9a\xe8\xbf\x87')]),
            preserve_default=True,
        ),
    ]
