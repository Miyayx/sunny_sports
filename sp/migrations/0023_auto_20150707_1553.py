# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0022_auto_20150707_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='address',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='contact_email',
            field=models.EmailField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='contact_name',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='contact_phone',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='contact_qq',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='contact_wx',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.CharField(max_length=20, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='leader',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='postno',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
    ]
