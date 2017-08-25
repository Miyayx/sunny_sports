# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_auto_20150419_2152'),
        ('sp', '0010_coachorg_ali_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachtrain',
            name='bill',
            field=models.OneToOneField(null=True, to='payment.Bill'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coachtrain',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x9c\xaa\xe4\xbb\x98\xe8\xb4\xb9'), (1, b'\xe5\xb7\xb2\xe4\xbb\x98\xe8\xb4\xb9')]),
            preserve_default=True,
        ),
    ]
