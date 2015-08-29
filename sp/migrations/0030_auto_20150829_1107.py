# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0029_auto_20150816_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='address',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='contact_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='contact_phone',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='contact_qq',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='leader',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='other_info',
            field=models.CharField(max_length=5000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='postno',
            field=models.CharField(max_length=80, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='teamevent',
            name='award',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x9a\x82\xe6\x97\xa0\xe7\xbb\x93\xe6\x9e\x9c'), (1, b'\xe4\xb8\x80\xe7\xad\x89\xe5\xa5\x96'), (2, b'\xe4\xba\x8c\xe7\xad\x89\xe5\xa5\x96'), (3, b'\xe4\xb8\x89\xe7\xad\x89\xe5\xa5\x96'), (4, b'\xe5\x8f\x82\xe8\xb5\x9b\xe5\xa5\x96'), (5, b'\xe7\xbc\xba\xe8\xb5\x9b')]),
        ),
    ]
