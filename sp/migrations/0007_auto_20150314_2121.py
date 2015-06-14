# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0006_train_pass_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermessage',
            name='user',
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.CharField(default=b'', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usermessage',
            name='userrole',
            field=models.ForeignKey(default=1, to='sp.UserRole'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='train',
            name='pass_status',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe5\xae\xa1\xe6\xa0\xb8'), (1, b'\xe5\xae\xa1\xe6\xa0\xb8\xe9\x80\x9a\xe8\xbf\x87'), (2, b'\xe5\xae\xa1\xe6\xa0\xb8\xe6\x9c\xaa\xe9\x80\x9a\xe8\xbf\x87')]),
            preserve_default=True,
        ),
    ]
