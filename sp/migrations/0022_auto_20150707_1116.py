# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0021_auto_20150704_2153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='fullname',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='contact_weixin',
            new_name='contact_wx',
        ),
        migrations.RemoveField(
            model_name='studentteam',
            name='stu_number',
        ),
        migrations.AlterField(
            model_name='teamevent',
            name='award',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x97\xa0\xe8\xae\xb0\xe5\xbd\x95'), (1, b'\xe4\xb8\x80\xe7\xad\x89\xe5\xa5\x96'), (2, b'\xe4\xba\x8c\xe7\xad\x89\xe5\xa5\x96'), (3, b'\xe4\xb8\x89\xe7\xad\x89\xe5\xa5\x96'), (4, b'\xe7\xbc\xba\xe8\xb5\x9b')]),
        ),
    ]
